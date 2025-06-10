import numpy as np
import lid_cavity.diff_operators as diff
from lid_cavity.SimulConfig import SimulConfig

class SimulResult:
    """
    Container class for storing and accessing the results of a 2D incompressible flow simulation.

    Attributes:
    -----------
    u : np.ndarray
        Horizontal velocity component array of shape (nt+1, nx+1, ny+1).
    v : np.ndarray
        Vertical velocity component array of shape (nt+1, nx+1, ny+1).
    pressure : np.ndarray
        Pressure field array of shape (nt, nx+1, ny+1).
    curl : np.ndarray
        Vorticity (scalar curl) field array, shape (nt, nx+1, ny+1)
    speed : np.ndarray
        Magnitude of velocity field: speed = sqrt(u² + v²) at each point, shape (nt+1, nx+1, ny+1) 
    """

    def __init__(self, u, v, pressure, curl, speed):
        self.u = u
        self.v = v
        self.pressure = pressure
        self.curl = curl
        self.speed = speed
