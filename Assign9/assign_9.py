"""Assignment 9: explicit, analytical, and implicit (Crank-Nicolson) solutions for a 1D rod."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from biomodeling.diffusion import open_output  # noqa: E402
from biomodeling.heat1d import analytical_table, crank_nicolson_table, finite_table  # noqa: E402


def problem1():
    a = np.array([[1, 2, 3, 4], [2, 4, 5, 6], [7, 8, 5, -2], [4, 1, 2, 3]])
    b = np.array([[5], [8], [1], [5]])
    print(np.linalg.solve(a, b))


def problem2():
    a = np.array([[0, -1, .24, 0, 0, .25],
                  [-2, 0, .49, 2, 1, .31],
                  [0, -3, 1.77, 0, 2, 1.55],
                  [0, 0, 1, 1, 0, 1],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1]])
    b = np.array([[0], [6], [12], [6], [3.46], [.785]])
    print(np.linalg.solve(a, b))


def save_table(table, file_name, header=""):
    with open_output(file_name) as out:
        np.savetxt(out, table, fmt="%.4f", delimiter=",", comments="", newline="\r\n", header=header)


def main():
    problem1()
    problem2()
    save_table(finite_table(), "Finite.txt")
    save_table(analytical_table(), "Analytical.txt")
    # the original implicit file has no x header row
    save_table(crank_nicolson_table()[1:], "Implicit.txt", header="implicit")


if __name__ == "__main__":
    main()
