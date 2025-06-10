import os
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from lid_cavity.SimulConfig import SimulConfig
from lid_cavity.GridConstr import GridConstr


class AnimationConfig: 

    def __init__(self, config: SimulConfig,  grid: GridConstr,  export_dir, frame_skip=50, downsample=2, interval=50):
            
            self.animation_time = config.T
            self.dt = config.dt
            self.nt = config.nt

            self.frame_skip = frame_skip
            self.downsample = downsample
            self.interval = interval

            self.export_dir = export_dir
            #self.filename = filename

            # Grid Configuration
            self.nx = grid.nx
            self.ny = grid.ny
            self.h = grid.h
            self.x = grid.x
            self.y = grid.y
            self.grid_x = grid.grid_x
            self.grid_y = grid.grid_y
            self.Lx = grid.Lx 
            self.Ly = grid.Ly
