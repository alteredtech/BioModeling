"""Assignment 7: heat diffusion in a 2D plate and a 3D cube (explicit finite differences)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from biomodeling.diffusion import (  # noqa: E402
    evolve, find_equilibrium, find_time, open_output, write_rows,
)

STEEL_ALPHA = 54 / (7800 * (0.46 * 10**3))


def make_plate(rows, cols, top_bottom_value, side_value):
    plate = np.zeros((rows, cols))
    plate[:, 0] = side_value
    plate[:, -1] = side_value
    plate[0] = top_bottom_value
    plate[-1] = top_bottom_value
    return plate


def make_cube(nz, ny, nx, side_value, bottom_value, center_value):
    cube = np.full((nz, ny, nx), float(center_value))
    cube[:, 0, :] = side_value
    cube[:, -1, :] = side_value
    cube[:, :, 0] = side_value
    cube[:, :, -1] = side_value
    cube[-1] = side_value
    cube[0] = bottom_value
    return cube


def plate_problem(header, dx, dy, dt, alpha, cols, rows, top_bottom_value, side_value,
                  target, file_name, report_every=25):
    """Heat a plate until the center reaches ``target``. Log it every ``report_every`` days."""
    plate = make_plate(rows, cols, top_bottom_value, side_value)
    center = (rows // 2, cols // 2)
    spacings = (dy, dx)
    last_step = round(find_time(plate, alpha, dt, spacings, center, target) / dt)
    every = round(report_every / dt)

    with open_output(file_name) as out:
        out.write(header + "\nTime: 0.0\n")
        write_rows(out, plate)
        for n, grid in evolve(plate, alpha, dt, spacings):
            if n % every == 0 or n == last_step:
                out.write(f"\nTime: {n * dt:.1f}\n")
                write_rows(out, grid)
            if n >= last_step:
                break


def cube_cross(header, dx, dy, dz, dt, alpha, side_value, bottom_value, center_value,
               nx, ny, nz, target, file_name):
    """Heat a cube until the center reaches ``target``. Save the x and y cross sections."""
    cube = make_cube(nz, ny, nx, side_value, bottom_value, center_value)
    center = (nz // 2, ny // 2, nx // 2)
    for _, grid in evolve(cube, alpha, dt, (dz, dy, dx)):
        if grid[center] >= target:
            break
    cross = np.vstack((grid[:, :, center[2]], grid[:, center[1], :]))
    with open_output(file_name) as out:
        write_rows(out, cross, header=header)


def cube_center_column(header, file_name, dx, dy, dz, dt, alpha, side_value, bottom_value,
                       center_value, nx, ny, nz, modulus, window, difference):
    """Log the center column of a cube every ``modulus`` steps until it nears equilibrium."""
    cube = make_cube(nz, ny, nx, side_value, bottom_value, center_value)
    center = (nz // 2, ny // 2, nx // 2)
    spacings = (dz, dy, dx)
    stop_at = round(find_equilibrium(cube, alpha, dt, spacings, center, window), 1) - difference

    with open_output(file_name) as out:
        out.write(header + "\n")
        for n, grid in evolve(cube, alpha, dt, spacings):
            done = grid[center] >= stop_at
            if n % modulus == 0 or done:
                column = grid[:, center[1], center[2]]
                out.write(f"Time:, {n * dt:.1f}, " + ",".join(f"{v:.4f}" for v in column) + "\r\n")
            if done:
                break


def main():
    cube_center_column("Cube Center", "CenterColumn.txt", 0.01, 0.01, 0.01, 1, STEEL_ALPHA,
                       40, 150, 20, 21, 21, 21, 50, 30, 0.1)


if __name__ == "__main__":
    main()
