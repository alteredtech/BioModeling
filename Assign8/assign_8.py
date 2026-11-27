"""Assignment 8: a candy bar (quarter model) cooling in air, with convection and a symmetry line."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from biomodeling.cooling import check_cooling_stability, step_cooling  # noqa: E402
from biomodeling.diffusion import open_output, write_rows  # noqa: E402

MAX_STEPS = 10**7


def cool(block, fo, bi, ambient):
    """Yield ``(step, grid)`` after each step. Stop after ``MAX_STEPS`` steps."""
    check_cooling_stability(fo, bi)
    for n in range(1, MAX_STEPS + 1):
        block = step_cooling(block, fo, bi, ambient)
        yield n, block
    raise RuntimeError(f"no result after {MAX_STEPS} steps")


def snickers(file_name, start_temp=33, target_temp=15, ambient=5, dt=0.01, dx=1 / 1000,
             conv_rate=100, therm_cond=0.4, heat_cap=2400, rho=800,
             n_x=16, n_y=11, probe=(10, 8)):
    """Cool the bar until ``probe`` (row, column) is below ``target_temp``.

    Write the grid at 25%, 50%, and 75% of the cooling time and at the end.
    """
    fo = (therm_cond / (rho * heat_cap)) * dt / dx**2
    bi = conv_rate * dx / therm_cond
    block = np.full((n_y, n_x), float(start_temp))

    def reached(grid):
        return round(grid[probe], 8) < target_temp

    last_step = next(n for n, grid in cool(block, fo, bi, ambient) if reached(grid))
    marks = {int((last_step - 1) * share) for share in (0.25, 0.5, 0.75)}

    with open_output(file_name) as out:
        out.write("Problem 8\n")
        for n, grid in cool(block, fo, bi, ambient):
            if n in marks or n == last_step:
                out.write(f"\nTime: {n * dt:.1f}\n")
                write_rows(out, grid)
            if n == last_step:
                break


def main():
    snickers("snickers.txt")


if __name__ == "__main__":
    main()
