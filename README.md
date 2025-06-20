# Computational Fluid Dynamics (CFD)

# 🌀 Lid-Driven Cavity Flow Solver

This project simulates the 2D lid-driven cavity flow problem — a benchmark case in computational fluid dynamics — using finite difference methods for incompressible Navier-Stokes equations.

The simulation is implemented in Python and visualized through velocity fields, streamlines, and animations.

---

## 📁 Repository Structure

├── main.ipynb # Jupyter Notebook to run the simulation<br>
├── lid_cavity/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── init.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── AnimationConfig.py # Animation settings for matplotlib<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── diff_operators.py # Central difference, Laplacian, divergence, curl<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── FramePlots.py # Functions for plotting velocity and streamlines<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── GridConstr.py # Grid generation<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── PlotConfig.py # Plotting configuration<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── SimulConfig.py # Simulation parameter configuration<br>
&nbsp;&nbsp;&nbsp;&nbsp;│ ├── SimulResult.py # Stores and processes simulation data<br>
└── Results/ # Stores visulaization as .mp4<br>



---

## ⚙️ Features

- Finite Difference Scheme (central difference, 5-point Laplacian)
- Modular simulation setup via config classes
- Velocity field, vorticity, and streamlines visualization
- Optional animation creation using Matplotlib
- Highly customizable: grid size, time step, Reynolds number, etc.

---

## 🧠 Physics Overview

The solver addresses the incompressible Navier-Stokes equations:

∂u/∂t + (u · ∇)u = -∇p + ν ∇²u
∇ · u = 0

- The domain is a square cavity.
- The top lid moves horizontally, inducing flow.
- No-slip boundary conditions on all walls.

---

## 🔧 Example 
https://github.com/user-attachments/assets/8354aa0f-e1cc-416c-82e2-b13c32095601

