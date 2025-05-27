# DeepMD for Anti-Perovskite Solid Electrolytes

This repository contains DeepMD models, AIMD datasets, and simulation scripts used to study lithium-ion transport and thermal properties in anti-perovskite solid electrolytes (AP SEs).

## Overview

We develop a deep learning-based interatomic potential using the Deep Potential Molecular Dynamics (DeepMD) framework. The model is trained on extensive AIMD data covering:

- Thermodynamic states  
- Lattice strains  
- Point defect types and concentrations  
- Halogen doping environments  

With this model, we quantitatively investigate:

- Lithium-ion diffusion  
- Thermal expansion  
- Thermal conductivity  

## Requirements

- DeepMD-kit  
- LAMMPS (with DeepMD support)  
- Python 3.x (NumPy, pandas, matplotlib)
<<<<<<< HEAD
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

**MSD fitting & conductivity**: `plot_msd&fit.py`

**Thermal expansion**: `analyze_thermal_expansion.py`

**Thermal conductivity (NEMD)**: `analyze_nemd.py`

## MLP Training

The `MLP Train Process/` directory contains:

- `input.json`: full DP training input
- `plot_loss.py`: script to visualize training/validation RMSE curves

**Energy, force, virial convergence** is benchmarked using validation RMSE curves output to `lcurve.out`.

=======
>>>>>>> parent of a834d80 (Upload)
