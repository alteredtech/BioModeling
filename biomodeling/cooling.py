"""Explicit 2D conduction with convection on three faces (Assign8, the candy-bar quarter model).

The top, left, and right faces lose heat to the air. The bottom face is a symmetry line, so it
is insulated. Each edge cell uses a mirrored neighbor, which gives the half-cell weights.
"""
import numpy as np


def check_cooling_stability(fo, bi):
    if fo * 4 * (1 + bi) > 1:
        raise ValueError(f"unstable: 4*fo*(1+bi) = {4 * fo * (1 + bi):.4f} > 1")


def step_cooling(u, fo, bi, ambient):
    """Return the grid after one time step. ``fo`` is the Fourier number, ``bi`` the Biot number."""
    p = np.pad(u, 1, mode="reflect")
    neighbors = p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]
    faces = np.zeros_like(u)
    faces[0, :] += 1   # top
    faces[:, 0] += 1   # left
    faces[:, -1] += 1  # right
    return u + fo * (neighbors - 4 * u) + 2 * bi * fo * faces * (ambient - u)
