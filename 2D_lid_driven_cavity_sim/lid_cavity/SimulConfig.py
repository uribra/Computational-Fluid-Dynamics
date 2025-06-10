import numpy as np 

class SimulConfig: 
    '''
    Simulation Configuration class for the lid driven cavity 

    Attributes:
    ------------
        Lx, Ly (float): Number of grid nodes in each dimension.
        h (float): Space discretization
        dt (float): Time discretizaton 
        T (float): Final time for simulation
        rho: (float): Fluid density
        nu (float): Kinematic viscosity
        lid_velocity (callable): Possible time dependent Lid velocity
        nx, ny (int): Number of grid points in each dimension
    """

    '''

    def __init__(self, Lx: float, Ly: float, h: float, dt: float, T: float,
             rho: float, nu: float, lid_velocity: callable,
             verbose: bool = True):

        self.Lx = Lx
        self.Ly = Ly
        self.h = h
        self.dt = dt
        self.T = T
        self.rho = rho
        self.nu = nu
        self.lid_velocity = lid_velocity  
        self.verbose = verbose
        self.nt = int(T/dt)
        self.nx = int(Lx/h)
        self.ny = int(Ly/h)
        if verbose:
            self.print_config()

    def print_config(self):
        print(f"Simulation Configuration for 2D lid-driven cavity flow:\n"
            f"--------------------------------------------------------\n"
            f"  Domain size: Lx = {self.Lx}, Ly = {self.Ly}\n"
            f"  Grid spacing: h = {self.h}\n"
            f"  Grid nodes: nx = {self.nx + 1}, ny = {self.ny + 1}\n"
            f"  Final time: T = {self.T}\n"
            f"  Time step: dt = {self.dt}\n"
            f"  Number of time steps: nt = {self.nt}\n"
            f"  Simulation time: T = {self.nt * self.dt}\n"
            f"  Fluid density: rho = {self.rho}\n"
            f"  Kinematic viscosity: nu = {self.nu}\n")

    
    def validate_SimulConfig(self) -> None:
        """
        Validates the SimulConfig parameters to ensure they are within acceptable ranges.
        """
        if self.Lx <=0 or self.Ly <= 0:
            raise ValueError("Lengths of the box Lx, Ly have to strictly positive.")
        if self.T <= 0:
            raise ValueError('Final time T has to be strictly positive.')
        if self.h <= 0:
            raise ValueError("Space discretization h must be strictly positive.")
        if self.dt <=0:
            raise ValueError("Time discretization dt must be strictly positive.")
        if self.rho <=0:
            raise ValueError("Fluid density rho must be strictly positive.")
        if self.nu <=0:
            raise ValueError("Kinematic viscosity nu must be strictly positive.")
        
        if not (callable(self.lid_velocity) or isinstance(self.lid_velocity, (list, tuple, np.ndarray))):
            raise TypeError("Lid velocity must be a function lid_velocity(t) or a list/array of velocity values.")
        if isinstance(self.lid_velocity, (np.ndarray, list, tuple)):
            if np.array(self.lid_velocity).ndim != 1:
                raise ValueError("lid_velocity must be 1D if passed as an array-like object.")



