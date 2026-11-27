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


# --- 1D tables (Assign6, Assign9) and cooling (Assign8) ---
from biomodeling.cooling import step_cooling  # noqa: E402
from biomodeling.heat1d import analytical_table, crank_nicolson_table, finite_table  # noqa: E402


def test_tables_have_same_layout_and_times():
    f, a, c = finite_table(), analytical_table(), crank_nicolson_table()
    assert f.shape == a.shape == c.shape == (102, 12)
    assert np.allclose(f[:, 0], a[:, 0]) and np.allclose(f[1:, 0], np.arange(101) * 0.001)


def test_finite_and_implicit_agree_with_analytical_at_same_time():
    f, a, c = finite_table(), analytical_table(), crank_nicolson_table()
    assert np.abs(f[11:, 1:] - a[11:, 1:]).max() < 0.02  # skip the first steps: the start profile has a kink
    assert np.abs(c[11:, 1:] - a[11:, 1:]).max() < 0.02


def loop_cooling(u, fo, bi, t):
    """The original per-cell equations from Assign8, kept as a reference."""
    ny, nx = u.shape
    new = np.zeros_like(u)
    for j in range(ny):
        for k in range(nx):
            top, bottom, left, right = j == 0, j == ny - 1, k == 0, k == nx - 1
            up = u[j - 1, k] if not top else u[j + 1, k]
            down = u[j + 1, k] if not bottom else u[j - 1, k]
            lf = u[j, k - 1] if not left else u[j, k + 1]
            rt = u[j, k + 1] if not right else u[j, k - 1]
            conv = (top + left + right) * 2 * bi * fo * (t - u[j, k])
            new[j, k] = u[j, k] + fo * (up + down + lf + rt - 4 * u[j, k]) + conv
    return new


def test_cooling_matches_explicit_corner_and_edge_formulas():
    rng = np.random.default_rng(1)
    u = rng.random((11, 16)) * 30
    fo, bi, t = 0.002, 0.25, 5.0
    new = step_cooling(u, fo, bi, t)
    assert np.allclose(new, loop_cooling(u, fo, bi, t))
    # hand-written original equations
    assert new[0, 0] == pytest.approx((1 - 4*fo - 4*bi*fo) * u[0, 0] + 2*fo*(u[0, 1] + u[1, 0] + 2*bi*t))
    assert new[10, 0] == pytest.approx((1 - 4*fo - 2*bi*fo) * u[10, 0] + 2*fo*(u[9, 0] + u[10, 1] + bi*t))
    assert new[10, 5] == pytest.approx((1 - 4*fo) * u[10, 5] + 2*fo*(u[9, 5] + .5*(u[10, 4] + u[10, 6])))
