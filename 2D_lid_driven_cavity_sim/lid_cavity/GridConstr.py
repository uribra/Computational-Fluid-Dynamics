import numpy as np
from lid_cavity.SimulConfig import SimulConfig


class GridConstr: 

    """
    Grid class for the lid-driven cavity simulation.

    Attributes:
    ------------
        Lx, Ly (float): Number of grid nodes in each dimension.
        nx+1, ny+1 (int): Number of grid nodes in each dimension.
        h (float): Space discretization parameter in x- and y-dimension.
        x (np.ndarray): Array of x-coordinates.
        y (np.ndarray): Array of y-coordinates.
        grid_x (np.ndarray): 2D meshgrid array for x-coordinates.
        grid_y (np.ndarray): 2D meshgrid array for y-coordinates.
    """

    def __init__(self, config: SimulConfig):
        """
        Initialize grid with provided simulation configuration.

        :param config: Simulation configuration.
        """
        self.Lx = config.Lx
        self.Ly = config.Ly
        self.nx = config.nx
        self.ny = config.ny
        self.h = config.h
        self.x = np.linspace(0., config.Lx, config.nx +1)
        self.y = np.linspace(0., config.Ly, config.ny +1)
        self.grid_x, self.grid_y = np.meshgrid(self.x, self.y) 

    def validate_GridConfig(self) -> None:
        """
        Validates the Grid Configuration parameters to ensure they are within acceptable ranges.
        """
        if self.Lx <=0 or self.Ly <= 0:
            raise ValueError("Lengths of the box Lx, Ly have to strictly positive.")
        if self.h <= 0:
            raise ValueError("Space discretization h must be strictly positive.")
