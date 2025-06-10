import os
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from lid_cavity.SimulResult import SimulResult
from lid_cavity.PlotConfig import PlotConfig


class FramePlots:
    def __init__(self, result: SimulResult, config: PlotConfig):

        self.export_dir = config.export_dir
        self.animation_time = config.T
        self.downsample = config.downsample

        # Extrac Grid configuration 
        self.grid_x = config.grid_x
        self.grid_y = config.grid_y  
        self.Lx = config.Lx
        self.Ly = config.Ly
        self.nt = config.nt
        self.dt = config.dt
        self.T = config.T

        # Extract simulation results
        self.u = result.u
        self.v = result.v
        self.pressure = result.pressure
        self.curl = result.curl
        self.speed = result.speed


    def plot_streamlines_frame(self, result: SimulResult, config: PlotConfig, frame_time, filename):

        frame_index = int(frame_time / self.dt)    
        u_n = self.u[frame_index]
        v_n = self.v[frame_index]
        speed_n = self.speed[frame_index]

        # Ensure output directory exists
        os.makedirs(self.export_dir, exist_ok=True)

        # Full path to save the animation
        save_path = os.path.join(self.export_dir, filename)

        plt.style.use("dark_background")
        plt.figure(figsize = (8,6))

        # Contour plot for the pressure
        #plt.contourf(config.grid_x[::self.downsample, ::self.downsample], config.grid_y[::self.downsample, ::self.downsample], p_n[::self.downsample, ::self.downsample], levels = 50, cmap='viridis')
        #plt.colorbar()
        # Contour plot for the speed
        plt.contourf(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], speed_n[::self.downsample, ::self.downsample], levels = 50, cmap='viridis')
        plt.colorbar()

        plt.streamplot(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], u_n[::self.downsample, ::self.downsample], v_n[::self.downsample, ::self.downsample], density=1.5, arrowsize=1, color="tab:cyan")
        plt.xlim((0, self.Lx))
        plt.ylim((0, self.Ly))
        plt.title(f'Velocity field and pressure at time step {frame_time:.2f}')
        plt.savefig(save_path)
        plt.show()



    def plot_velocity_frame(self, frame_time, filename = "velocity_field.png"):

        frame_index = int(frame_time / self.dt)    
        u_n = self.u[frame_index]
        v_n = self.v[frame_index]
        speed_n = self.speed[frame_index]

        # Ensure output directory exists
        os.makedirs(self.export_dir, exist_ok=True)

        # Full path to save the animation
        save_path = os.path.join(self.export_dir, filename)


        plt.style.use("dark_background")
        plt.figure(figsize = (8,6))

        # Contour plot for the pressure
        #plt.contourf(config.grid_x[::self.downsample, ::self.downsample], config.grid_y[::self.downsample, ::self.downsample], p_n[::self.downsample, ::self.downsample], levels = 50, cmap='viridis')
        #plt.colorbar()
        # Contour plot for the speed
        plt.contourf(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], speed_n[::self.downsample, ::self.downsample], levels = 50, cmap='viridis')
        plt.colorbar()

        plt.quiver(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], u_n[::self.downsample, ::self.downsample], v_n[::self.downsample, ::self.downsample], arrowsize=1, color="tab:cyan")
        plt.xlim((0, self.Lx))
        plt.ylim((0, self.Ly))
        plt.title(f'Velocity field and pressure at time step {frame_time:.2f}')
        plt.savefig(save_path)
        plt.show()

