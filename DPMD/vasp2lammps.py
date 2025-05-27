from ase.io import read, write
from ase.data import atomic_numbers

# === Step 1: Read structure from POSCAR file ===
# Load the atomic structure from a VASP-format POSCAR file using ASE
atoms = read('POSCAR', format='vasp')

# === Step 2: Write to an intermediate LAMMPS data file ===
# Export the structure to a temporary LAMMPS data file without guaranteed type-ID order
write('lammps_unsorted.data', atoms, format='lammps-data', atom_style='atomic')

# === Step 3: Reload and assign correct atomic numbers by type-ID mapping ===
# Manually define type-to-element mapping to ensure LAMMPS type-ID corresponds to correct atomic species
atoms_lammps = read('lammps_unsorted.data', format='lammps-data', style='atomic',
                    Z_of_type={
                        1: atomic_numbers['Li'], 
                        2: atomic_numbers['Cl'], 
                        3: atomic_numbers['O'], 
                        4: atomic_numbers['Br']
                    })

# === Step 4: Write the corrected structure to the final LAMMPS data file ===
# Save the properly sorted and labeled structure into a standard LAMMPS data file
write('lammps.data', atoms_lammps, format='lammps-data', atom_style='atomic')