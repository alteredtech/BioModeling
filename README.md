# BioModeling

Coursework for a biological and engineering modeling class: finite-difference models of heat
diffusion, predator-prey dynamics, and linear systems, written in Python with NumPy.

## Layout

- `biomodeling/diffusion.py` - vectorized explicit diffusion solver (1D, 2D, 3D) with a
  stability check and a step limit.
- `Assign1/` ... `Assign9/`, `Quiz1/` - one folder for each assignment. `Assign7/assign_7.py` uses the
  shared solver. The other scripts are still the original versions.
- `tests/` - `pytest` tests (loop-versus-vectorized check, analytic rod solution, safety limits).

## Run

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python Assign7/assign_7.py     # writes to output/ (git-ignored)
pytest
```
