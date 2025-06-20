# Computational Fluid Dynamics (CFD)

# 🌀 Lid-Driven Cavity Flow Solver

This project simulates the 2D lid-driven cavity flow problem — a benchmark case in computational fluid dynamics — using finite difference methods for incompressible Navier-Stokes equations.

The simulation is implemented in Python and visualized through velocity fields, streamlines, and animations.

---

## 📁 Repository Structure

├── main.ipynb # Jupyter Notebook to run the simulation
├── diff_operators.py # Numerical differentiation operators
├── AnimationConfig.py # Configuration for animation settings
├── FramePlots.py # Frame plotting utilities (velocity, streamlines)
├── lid_cavity/ # (Expected) Core simulation modules: SimulConfig, GridConstr, SimulResult, PlotConfig


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

\[
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u}
\]
\[
\nabla \cdot \mathbf{u} = 0
\]

- The domain is a square cavity.
- The top lid moves horizontally, inducing flow.
- No-slip boundary conditions on all walls.

---



https://github.com/user-attachments/assets/8354aa0f-e1cc-416c-82e2-b13c32095601

