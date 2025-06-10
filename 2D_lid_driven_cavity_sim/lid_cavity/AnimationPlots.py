import os
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from lid_cavity.SimulResult import SimulResult
from lid_cavity.AnimationConfig import AnimationConfig


class Animation:
    def __init__(self, result: SimulResult, config: AnimationConfig):

        self.export_dir = config.export_dir
        self.animation_time = config.T

        self.frame_skip = config.frame_skip
        self.downsample = config.downsample
        self.interval = config.interval

        # Extrac Grid configuration 
        self.grid_x = config.grid_x
        self.gird_y = config.grid_y  
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


    def plot_streamlines(self, filename = "streamlines.mp4"):

        """
        Save animation of streamlines of the velocity field and pressure fields as an .mp4 video in a specific folder.
        """

        # Ensure output directory exists
        os.makedirs(self.export_dir, exist_ok=True)

        # Full path to save the animation
        save_path = os.path.join(self.export_dir, filename)

        fig, ax = plt.subplots(figsize=(6, 6))

        def frame_func(u_k, v_k, p_k, k):
            ax.clear()
            contour = ax.contourf(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], p_k[::self.downsample, ::self.downsample], levels = 50, cmap='viridis')
            ax.colorbar()
            ax.streamplot(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], u_k[::self.downsample, ::self.downsample], v_k[::self.downsample, ::self.downsample], density=1.5, arrowsize=1, color="tab:cyan")
            ax.set_xlim((0, self.Lx))
            ax.set_ylim((0, self.Ly))
            ax.set_title(f"Velocity and Pressure Field at t = {k * self.dt:.2f}")
            return contour

        def animate(k):
            frame_func(self.u[k+1], self.v[k+1], self.p[k], k)

        anim = FuncAnimation(fig, animate, interval = self.interval , frames = range(0, self.nt, self.frame_skip), repeat=False)

        writer = FFMpegWriter(fps=15, metadata=dict(artist='Your Name'), bitrate = 1800)
        anim.save(save_path, writer=writer)

    def plot_velocity(self, filename = "velocity_field.mp4"):

        """
        Save animation of velocity and pressure fields as an .mp4 video in a specific folder.
        """

        # Ensure output directory exists
        os.makedirs(self.export_dir, exist_ok=True)

        # Full path to save the animation
        save_path = os.path.join(self.export_dir, filename)

        fig, ax = plt.subplots(figsize=(6, 6))

        def frame_func(u_k, v_k, p_k, k):
            ax.clear()
            contour = ax.contourf(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], p_k[::self.downsample, ::self.downsample], levels = 50, cmap='viridis')
            ax.colorbar()
            ax.quiver(self.grid_x[::self.downsample, ::self.downsample], self.grid_y[::self.downsample, ::self.downsample], u_k[::self.downsample, ::self.downsample], v_k[::self.downsample, ::self.downsample], arrowsize=1, color='black')
            ax.set_xlim((0, self.Lx))
            ax.set_ylim((0, self.Ly))
            ax.set_title(f"Velocity and Pressure Field at t = {k * self.dt:.2f}")
            return contour

        def animate(k):
            frame_func(self.u[k+1], self.v[k+1], self.p[k], k)

        anim = FuncAnimation(fig, animate, interval=self.interval , frames = range(0, self.nt, self.frame_skip), repeat=False)

        writer = FFMpegWriter(fps=15, metadata=dict(artist='Your Name'), bitrate = 1800)
        anim.save(save_path, writer=writer)        







