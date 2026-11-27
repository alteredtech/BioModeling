import numpy as np
import pytest

from biomodeling.diffusion import (
    check_stability, evolve, find_equilibrium, find_time, step,
)


def loop_step_2d(u, alpha, dt, dy, dx):
    """The original per-cell loops, kept as a reference."""
    new = u.copy()
    for i in range(1, u.shape[0] - 1):
        for j in range(1, u.shape[1] - 1):
            fx = alpha * (u[i, j + 1] - 2 * u[i, j] + u[i, j - 1]) / dx**2 * dt
            fy = alpha * (u[i + 1, j] - 2 * u[i, j] + u[i - 1, j]) / dy**2 * dt
            new[i, j] = fx + fy + u[i, j]
    return new


def test_step_matches_loop_reference_2d():
    rng = np.random.default_rng(0)
    u = rng.random((11, 21))
    assert np.allclose(step(u, 2.83e-5, 0.1, (0.01, 0.02)), loop_step_2d(u, 2.83e-5, 0.1, 0.01, 0.02))


def test_step_keeps_boundaries_and_input():
    u = np.arange(25.0).reshape(5, 5)
    before = u.copy()
    new = step(u, 1.0, 0.01, (1.0, 1.0))
    assert np.array_equal(u, before)
    assert np.array_equal(new[0], u[0]) and np.array_equal(new[:, -1], u[:, -1])


def test_1d_rod_approaches_analytic_solution():
    # u(x,0)=sin(pi x), u(0)=u(1)=0, alpha=1  ->  u(x,t)=exp(-pi^2 t) sin(pi x)
    x = np.linspace(0, 1, 51)
    dx, dt = x[1] - x[0], 1e-4
    u = np.sin(np.pi * x)
    for n, grid in evolve(u, 1.0, dt, (dx,), max_steps=1000):
        if n == 1000:
            break
    assert np.allclose(grid, np.exp(-np.pi**2 * 0.1) * np.sin(np.pi * x), atol=1e-3)


def test_unstable_step_is_rejected():
    with pytest.raises(ValueError):
        check_stability(1.0, 1.0, (0.1,))
    with pytest.raises(ValueError):
        next(evolve(np.zeros(5), 1.0, 1.0, (0.1,)))


def test_max_steps_stops_endless_loop():
    u = np.zeros((5, 5))
    with pytest.raises(RuntimeError):
        find_time(u, 1e-5, 0.1, (0.01, 0.01), (2, 2), 1.0, max_steps=50)


def test_find_time_and_equilibrium_on_heated_rod():
    u = np.zeros(21)
    u[0] = u[-1] = 100.0
    args = (1.0, 1e-3, (0.05,))
    assert find_time(u, *args, (10,), 50.0) > 0
    assert find_equilibrium(u, *args, (10,), 10) == pytest.approx(100.0, abs=0.5)
