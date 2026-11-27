"""1D heat-conduction tables used by Assign6 and Assign9.

Every table has this layout: the first row is ``[0, x_0, x_1, ...]`` and each next row is
``[t, u(x_0, t), u(x_1, t), ...]`` for t = 0, dt, 2*dt, ... up to the final time.
The rod ends are held at 0.
"""
import numpy as np

from .diffusion import check_stability, step


def triangle(n_x, dx):
    """Initial profile: 2x for x <= 0.5 and 2(1-x) after it."""
    x = np.arange(n_x) * dx
    return np.where(np.arange(n_x) < int(n_x / 2 + 1), 2 * x, 2 * (1 - x))


def with_axes(profiles, dt, dx):
    """Add the x header row and the time column to a (steps, n_x) array."""
    n_steps, n_x = profiles.shape
    body = np.column_stack((np.arange(n_steps) * dt, profiles))
    header = np.concatenate(([0.0], np.arange(n_x) * dx))
    return np.vstack((header, body))


def finite_table(alpha=1.0, dt=0.001, dx=0.1, final_time=0.1, n_x=11):
    check_stability(alpha, dt, (dx,))
    u = triangle(n_x, dx)
    rows = [u]
    for _ in range(round(final_time / dt)):
        u = step(u, alpha, dt, (dx,))
        rows.append(u)
    return with_axes(np.array(rows), dt, dx)


def analytical_table(alpha=1.0, dt=0.001, dx=0.1, final_time=0.1, n_x=11, terms=1000):
    """Fourier-series solution: u = 8/pi^2 * sum (1/n^2) sin(n pi/2) sin(n pi x) exp(-alpha n^2 pi^2 t)."""
    x = np.arange(n_x) * dx
    t = np.arange(round(final_time / dt) + 1) * dt
    n = np.arange(1, terms)[:, None, None]
    series = (np.sin(n * np.pi / 2) / n**2) * np.sin(n * np.pi * x) * np.exp(-alpha * n**2 * np.pi**2 * t[:, None])
    profiles = 8 / np.pi**2 * series.sum(axis=0)
    profiles[0] = triangle(n_x, dx)
    profiles[:, 0] = 0.0
    profiles[:, -1] = 0.0
    return with_axes(profiles, dt, dx)


def crank_nicolson_table(alpha=1.0, dt=0.001, dx=0.1, final_time=0.1, n_x=11):
    """Implicit (Crank-Nicolson) solution with the same layout as ``finite_table``."""
    r = alpha * dt / dx**2
    a = np.diag(np.full(n_x, 2 + 2 * r)) + np.diag(np.full(n_x - 1, -r), 1) + np.diag(np.full(n_x - 1, -r), -1)
    a[0, :] = 0.0
    a[-1, :] = 0.0
    a[0, 0] = a[-1, -1] = 1.0
    u = triangle(n_x, dx)
    rows = [u]
    for _ in range(round(final_time / dt)):
        rhs = np.zeros(n_x)
        rhs[1:-1] = r * u[:-2] + (2 - 2 * r) * u[1:-1] + r * u[2:]
        u = np.linalg.solve(a, rhs)
        rows.append(u)
    return with_axes(np.array(rows), dt, dx)
