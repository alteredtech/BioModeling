# BioModeling

Coursework for a biological and engineering modeling class: finite-difference models of heat
diffusion, predator-prey dynamics, and linear systems, written in Python with NumPy.

## Layout

- `biomodeling/` - shared solvers: `diffusion.py` (vectorized 1D/2D/3D explicit diffusion with a
  stability check and a step limit), `heat1d.py` (rod tables: explicit, analytical, Crank-Nicolson),
  and `cooling.py` (2D conduction with convection).
- `Assign1/` ... `Assign9/`, `Quiz1/` - one folder for each assignment. `Assign6`, `7`, `8`, and `9` use the
  shared solvers. The other scripts are the original versions.
- `tests/` - `pytest` tests (loop-versus-vectorized check, analytic rod solution, safety limits).

## Run

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python Assign7/assign_7.py     # writes to output/ (git-ignored)
pytest
```
