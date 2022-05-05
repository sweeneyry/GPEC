import numpy as np

# Hi Zimi

def analytic_dipole(x_obs, y_obs, x_c, y_c, Bo, mu_r, r_weld):
    mu_0 = 4e-7 * np.pi
    x = x_obs - x_c
    y = y_obs - y_c
    r = np.sqrt(x**2 + y**2)
    M = Bo * (mu_r - 1)/(mu_0 * (mu_r + 1)/2)

    area = np.pi * r_weld**2

    Bx = (mu_0 * area/(2*np.pi*r**4)) * (M * 2*x*y)
    By = (mu_0 * area/(2*np.pi*r**4)) * (M * (-x**2 + y**2))

    return np.array([Bx, By])