import numpy as np
from tqdm import trange

import lid_cavity.diff_operators as diff
from lid_cavity.SimulConfig import SimulConfig
from lid_cavity.GridConstr import GridConstr
from lid_cavity.SimulResult import SimulResult

class LidDrivenCavity:
    """
    Simulation Configuration class for the lid-driven cavity.

    Attributes:
    -----------
        Lx, Ly (float): Physical dimensions of the domain.
        h (float): Grid spacing.
        dt (float): Time step size.
        nt (int): Number of time steps.
        rho (float): Fluid density.
        nu (float): Kinematic viscosity.
        lid_velocity (Callable): Time-dependent lid velocity function.
    """

    def __init__(self, config: SimulConfig, grid: GridConstr):

        self.Lx = config.Lx
        self.Ly = config.Ly
        self.h = config.h
        self.dt = config.dt
        self.nt = config.nt
        self.rho = config.rho
        self.nu = config.nu
        self.lid_velocity = config.lid_velocity
        self.verbose = config.verbose

        self.xx = grid.x
        self.yy = grid.y
        self.nx = grid.nx
        self.ny = grid.ny

        self.grid_x = grid.grid_x 
        self.grid_y = grid.grid_y 

        # Allocate storage arrays to store velocities, pressure, curl and speed
        self.u = np.zeros((self.nt+1, self.nx + 1, self.ny + 1))
        self.v = np.zeros((self.nt+1, self.nx + 1, self.ny + 1))
        self.pressure = np.zeros((self.nt, self.nx + 1, self.ny + 1))
        self.curl = np.zeros((self.nt+1, self.nx + 1, self.ny + 1))
        self.speed = np.zeros((self.nt+1, self.nx + 1, self.ny + 1))

        # Catch numerical instability
        if self.dt > 0.5 * (self.h**2 / self.nu):
            raise RuntimeError(f"Unstable system: dt = {self.dt}, max allowed = {0.5 * (self.h**2 / self.nu)}")

    
    def apply_boundary_conditions(self, u, v, u_lid):
        # 1. Component (horizontal component)
        # bottom and top boundary walls (BE CAREFUL where we define the lid to be, iparticular with the pressure poission equation)
        u[0, :] = 0.0
        u[-1, :] = u_lid 
        # Left and right boundary walls
        u[:, 0] = 0.0
        u[:, -1] = 0.0 

        # 2. Component (vertical component)
        v[:, 0] = 0.0
        v[:, -1] = 0.0
        v[0, :] = 0.0
        v[-1, :] = 0.0

        return u, v

    def one_step_intermediate(self, u, v, du_dx, du_dy, dv_dx, dv_dy, laplace_u, laplace_v):
        dt = self.dt
        u_star = u + dt*( - (u*du_dx + v*du_dy) + self.nu*laplace_u)
        v_star = v + dt*( -  (u*dv_dx + v*dv_dy) + self.nu*laplace_v )
        return u_star, v_star
    
    def correct_velocities(self, u_star, v_star, p):
        dt = self.dt
        h = self.h
        # Compute the discrete derivatives for the pressure
        dp_dx = diff.central_difference_x(p,h)
        dp_dy = diff.central_difference_y(p,h)
        # Compute the update for the velocities
        u_next = u_star - dt*dp_dx
        v_next = v_star - dt*dp_dy
        return u_next, v_next

    def rhs_pressure_poisson(self, u, v):
        h = self.h
        dt = self.dt
        rho = self.rho
        divergence_velocity = diff.divergence(np.array([u,v]), h)
        rhs = (rho / dt)* divergence_velocity
        return rhs 

    def pressure_poisson_solver(self, rhs, iter = 100):
        nx = self.nx 
        ny = self.ny
        h = self.h
        p_prev = np.zeros((ny + 1, nx + 1))
        for _ in range(iter):
            p_next = np.zeros_like(p_prev)
            # Update by Jacobi Iteration
            p_next[1:-1, 1:-1] = 1/4 * (+p_prev[1:-1, 0:-2] + p_prev[0:-2, 1:-1] + p_prev[1:-1, 2:  ] + p_prev[2:  , 1:-1] - h**2*rhs[1:-1, 1:-1])

            # Pressure Boundary Conditions: Homogeneous zero Neumann Boundary
            # Conditions everywhere except for the top, where it is a homogeneous zero Dirichlet bc 
            p_next[:, -1] = p_next[:, -2]
            p_next[0,  :] = p_next[1,  :]
            p_next[:,  0] = p_next[:,  1]
            p_next[-1, :] = 0.0

            p_prev = p_next
        
        return p_prev


    def run(self) -> SimulResult:
        
        nx = self.nx
        ny = self.ny 
        nt = self.nt
        h = self.h
        dt = self.dt

        if self.verbose: 
            print('Running simulation:')

        # Add the boundary condition to the initial condition with the initial lid velocity
        self.u[0], self.v[0] = self.apply_boundary_conditions(self.u[0], self.v[0], self.lid_velocity(0))
        self.curl[0] = diff.curl(np.array([self.u[0], self.v[0]]), h)
        self.speed[0] = np.sqrt(self.u[0]**2 + self.v[0]**2)

        for n in trange(nt):

            u_prev = self.u[n]
            v_prev = self.v[n]

            # Compute discrete differential operators (in space) for the velocity field component at time step t = n*dt
            du_prev_dx = diff.central_difference_x(u_prev, h)
            du_prev_dy = diff.central_difference_y(u_prev, h)
            dv_prev_dx = diff.central_difference_x(v_prev, h)
            dv_prev_dy = diff.central_difference_y(v_prev, h)
            laplace_u_prev = diff.laplace(u_prev, h)
            laplace_v_prev = diff.laplace(v_prev, h)

            # Compute intermediate velocities 
            u_star, v_star = self.one_step_intermediate(u_prev, v_prev, du_prev_dx, du_prev_dy, dv_prev_dx, dv_prev_dy, laplace_u_prev, laplace_v_prev)

            # Add the boundary conditions for intermediate velocties (lid_velocity allowed to be time dependent)
            u_star, v_star = self.apply_boundary_conditions(u_star, v_star, self.lid_velocity(n*dt))
            
            # Compute the right hand side for the pressure poission equation 
            rhs = self.rhs_pressure_poisson(u_star, v_star)

            # Solve the pressure poission equation and save the pressure
            #p = pressure_poisson(h, rhs)
            #pressure[n] = p
            p = self.pressure_poisson_solver(rhs)
            self.pressure[n] = p

            # Correct the velocities for the incompressibility condition to hold
            u_next, v_next = self.correct_velocities(u_star, v_star, p)

            # Add the boundary conditions to the updated velocties 
            u_next, v_next = self.apply_boundary_conditions(u_next, v_next, self.lid_velocity((n+1)*dt))
            
            # Store updated velocties
            self.u[n+1] = u_next
            self.v[n+1] = v_next

            # Compute curl and speed 
            self.curl[n+1] = diff.curl(np.array([self.u[n+1], self.v[n+1]]), h)
            self.speed[n+1] = np.sqrt(self.u[n+1]**2 + self.v[n+1]**2)

        # Pass the simulation results to SimulResult
        return SimulResult(u = self.u, v = self.v, pressure = self.pressure, curl = self.curl, speed = self.speed)    


    def plot_velocity_field(self):
        pass
    def plot_pressure_field(self):
        pass




