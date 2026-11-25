# Deep Potential model for antiperovskite solid electrolytes

Training input and analysis scripts for Li₃OCl₁₋ₓBrₓ. The Deep Potential uses a `se_e2_a` descriptor with a 6.0 Å cutoff and is trained for 800,000 steps. LAMMPS type order is Li, Cl, O, Br.

## Model Overview

- **System**: antiperovskite Li₃OCl₁₋ₓBrₓ
- **Framework**: DeePMD-kit and LAMMPS
- **Model format**: compressed `.pb` file for `pair_style deepmd`
- **Ion transport**: NVT, 1 fs timestep, 100 ps equilibration excluded from the MSD, 1 ns production. End-member benchmarks use 10 ns.
- **Temperatures**: 600, 800, 1000, 1200, and 1400 K. Room-temperature diffusivity is an Arrhenius extrapolation.
- **Conductivity**: Nernst–Einstein relation with \(n = N_{\mathrm{Li}}/V\) and \(H_R = 1\), evaluated at the production temperature.
- **Thermal expansion**: NPT from 300 to 1000 K in 100 K steps.
- **Lattice thermal conductivity**: 8× replication along the flow direction, 100 ps NPT and 500 ps NVT equilibration, then 2 ns NVE with Langevin regions at 400 K and 200 K. The reported value uses the final 1 ns and \(\kappa = J/|\mathrm{d}T/\mathrm{d}x|\).


## Requirements

- DeepMD-kit  
- LAMMPS (with DeepMD support)  
- Python 3.x (NumPy, pandas, matplotlib)
- ASE

## How to Use

### 1. Convert structures

```bash
python vasp2lammps.py  # Convert POSCAR to LAMMPS-compatible data file
```

### 2. Run DeepMD-based LAMMPS simulation

```lmp
pair_style   deepmd ../AP-compress.pb
pair_coeff   * *
```

### 3. Analyze

**Li⁺ Trajectories**: `plot_Li_migration_XY.py`

**MSD fitting and conductivity** at the production temperature: `python "plot_msd&fit.py" 1000`

**Thermal expansion**: `analyze_thermal_expansion.py`

**Thermal conductivity (NEMD)**: `analyze_nemd.py`

## MLP Training

The `MLP Train Process/` directory contains:

- `input.json`: full DP training input
- `plot_loss.py`: script to visualize training/validation RMSE curves

**Energy, force, virial convergence** is benchmarked using validation RMSE curves output to `lcurve.out`.
