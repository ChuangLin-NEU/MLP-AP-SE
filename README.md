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
