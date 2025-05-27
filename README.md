# Deep Potential MLP Model for Anti-Perovskite Solid Electrolytes

This repository provides the machine learning potential (MLP) and related training/analysis scripts for the study of anti-perovskite solid electrolytes (AP SEs) using the Deep Potential (DP) framework. 
The developed model enables accurate and efficient molecular dynamics simulations for investigating both ionic conductivity and thermal properties.

## Model Overview

- **System**: Anti-perovskite Li₃OCl₁₋ₓBrₓ  
- **Framework**: Deep Potential Molecular Dynamics (DeePMD-kit)  
- **Training data**: AIMD trajectories of defective/doped AP-SEs  
- **Model format**: Compressed `.pb` file compatible with `pair_style deepmd` in LAMMPS  
- **Application**: Nanosecond-scale MD simulations for ionic transport, thermal conductivity (NEMD), structure–property analysis  


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

**MSD fitting & conductivity**: `plot_msd&fit.py`

**Thermal expansion**: `analyze_thermal_expansion.py`

**Thermal conductivity (NEMD)**: `analyze_nemd.py`

## MLP Training

The `MLP Train Process/` directory contains:

- `input.json`: full DP training input
- `plot_loss.py`: script to visualize training/validation RMSE curves

**Energy, force, virial convergence** is benchmarked using validation RMSE curves output to `lcurve.out`.
