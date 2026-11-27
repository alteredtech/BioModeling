"""Assignment 6: 1D heat conduction in a rod (finite difference versus analytical)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from biomodeling.diffusion import evolve, open_output  # noqa: E402
from biomodeling.heat1d import analytical_table, finite_table, triangle  # noqa: E402

STEEL_ALPHA = (54 / (7800 * 0.046)) / 10**3
COPPER_ALPHA = (386 / (8960 * 0.038)) / 10**3


def save_table(table, file_name):
    with open_output(file_name) as out:
        np.savetxt(out, table, fmt="%.4f", delimiter=",", comments="", newline="\r\n")


def rod_until_center_below(file_name, initial, alpha, dt, dx, stop_value, log_every=None):
    """Cool a rod until its center is at or below ``stop_value``.

    Log the first row, the last row, and (when ``log_every`` is a time) every ``log_every`` rows.
    """
    center = len(initial) // 2
    every = 1 if log_every is None else round(log_every / dt)
    rows = [np.concatenate(([0.0], initial))]
    for n, u in evolve(initial, alpha, dt, (dx,), max_steps=10**8):
        done = u[center] <= stop_value
        if n % every == 0 or done:
            rows.append(np.concatenate(([n * dt], u)))
        if done:
            break
    save_table(np.array(rows), file_name)


def main():
    save_table(finite_table(), "finite.txt")
    save_table(analytical_table(), "analytical.txt")
    # Problem 4: triangle profile, until the center falls to 0.5
    rod_until_center_below("Problem4.txt", triangle(11, 0.1), 1.0, 0.001, 0.1, 0.5)
    # Problem 5: a rod at 100 with 0 at both ends, until the center falls to 20
    hot = np.full(11, 100.0)
    hot[0] = hot[-1] = 0.0
    rod_until_center_below("Problem5steel.txt", hot, STEEL_ALPHA, 0.001, 0.1, 20, log_every=100)
    rod_until_center_below("Problem5copper.txt", hot, COPPER_ALPHA, 0.001, 0.1, 20, log_every=100)


if __name__ == "__main__":
    main()
