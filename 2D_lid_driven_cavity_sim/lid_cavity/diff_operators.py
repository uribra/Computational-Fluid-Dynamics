import numpy as np 

def central_difference_x(f, h):
    df_dx = np.zeros_like(f)
    df_dx[1:-1, 1:-1] = ( f[1:-1, 2: ] - f[1:-1, 0:-2]) / (2 * h)
    return df_dx

def central_difference_y(f, h):
    df_dy = np.zeros_like(f)
    df_dy[1:-1, 1:-1] = ( f[2: , 1:-1]  - f[0:-2, 1:-1]) / (2 * h)
    return df_dy

def laplace(f, h):
    delta_f = np.zeros_like(f)
    delta_f[1:-1, 1:-1] = ( f[1:-1, 0:-2] + f[0:-2, 1:-1] - 4*f[1:-1, 1:-1] + f[1:-1, 2:  ] + f[2:  , 1:-1]) / (h**2)
    return delta_f

def divergence(F, h):
    divF = central_difference_x(F[0], h) + central_difference_y(F[1], h)
    return divF

def curl(F, h):
    curlF = central_difference_x(F[1], h) - central_difference_y(F[0], h)
    return curlF 


