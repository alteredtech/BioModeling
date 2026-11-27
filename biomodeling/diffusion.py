"""Explicit finite-difference diffusion on a regular 1D, 2D, or 3D grid.

Axes follow NumPy order: for a 3D array the axes are (z, y, x), and
``spacings`` lists the grid spacing in the same order. Boundary cells never
change, so they act as fixed-value (Dirichlet) boundaries.
"""
from collections import deque
from pathlib import Path

import numpy as np

DEFAULT_MAX_STEPS = 1_000_000


def stability_number(alpha, dt, spacings):
    """Return alpha*dt*sum(1/d**2). The explicit scheme needs this <= 0.5."""
    return alpha * dt * sum(1.0 / d**2 for d in spacings)


def check_stability(alpha, dt, spacings):
    """Raise ValueError when the explicit scheme would be unstable."""
    number = stability_number(alpha, dt, spacings)
    if number > 0.5:
        raise ValueError(
            f"unstable: alpha*dt*sum(1/d^2) = {number:.4f} > 0.5; reduce dt or increase the spacing"
        )


def step(u, alpha, dt, spacings):
    """Return the grid after one explicit time step. The input is not changed."""
    if u.ndim != len(spacings):
        raise ValueError("need one spacing for each axis")
    inner = (slice(1, -1),) * u.ndim
    change = 0.0
    for axis, d in enumerate(spacings):
        lo, hi = [slice(1, -1)] * u.ndim, [slice(1, -1)] * u.ndim
        lo[axis], hi[axis] = slice(0, -2), slice(2, None)
        second = (u[tuple(hi)] - 2 * u[inner] + u[tuple(lo)]) / d**2
        change = change + alpha * second * dt
    new = u.copy()
    new[inner] = u[inner] + change
    return new


def evolve(u, alpha, dt, spacings, max_steps=DEFAULT_MAX_STEPS):
    """Yield ``(step_number, grid)`` after each step, starting at step 1.

    Raise RuntimeError when the caller keeps iterating past ``max_steps``.
    """
    check_stability(alpha, dt, spacings)
    current = u
    for n in range(1, max_steps + 1):
        current = step(current, alpha, dt, spacings)
        yield n, current
    raise RuntimeError(f"no result after {max_steps} steps")


def find_time(u, alpha, dt, spacings, index, target, max_steps=DEFAULT_MAX_STEPS):
    """Return the time at which ``u[index]`` first reaches ``target``."""
    if u[index] >= target:
        return 0.0
    for n, grid in evolve(u, alpha, dt, spacings, max_steps):
        if grid[index] >= target:
            return n * dt


def find_equilibrium(u, alpha, dt, spacings, index, window, max_steps=DEFAULT_MAX_STEPS):
    """Return the value at ``index`` when it stops changing at 2 decimals.

    The value counts as settled when the mean of the last ``window`` values
    equals the current value, rounded to 2 decimals.
    """
    recent = deque(maxlen=window)
    for _, grid in evolve(u, alpha, dt, spacings, max_steps):
        value = grid[index]
        if len(recent) == window:
            mean = sum(recent) / window
            if round(mean, 2) == round(value, 2):
                return round(mean, 2)
        recent.append(value)


def write_rows(handle, array, header=None):
    """Write a 2D array as CSV text with CRLF line ends, as the course expects."""
    np.savetxt(handle, array, fmt="%.4f", delimiter=",", comments="", newline="\r\n", header=header or "")


def open_output(name, output_dir="output"):
    """Open ``output_dir/name`` for text writing and create the folder when needed."""
    path = Path(output_dir) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    return open(path, "w", newline="")
