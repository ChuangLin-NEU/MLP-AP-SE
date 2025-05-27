import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Set global font style
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'  # For consistent LaTeX-style superscripts

# ==========================
# Read LAMMPS data file to get initial structure
# ==========================
def read_lammps_data(filepath, scale=1.2):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    atoms_section = False
    atoms = []

    for i, line in enumerate(lines):
        if "xlo xhi" in line:
            x_bounds = list(map(float, line.strip().split()[0:2]))
        elif "ylo yhi" in line:
            y_bounds = list(map(float, line.strip().split()[0:2]))
        elif "zlo zhi" in line:
            z_bounds = list(map(float, line.strip().split()[0:2]))
        elif "Atoms" in line:
            atoms_section = True
            header_line = i + 1
        elif atoms_section and i > header_line:
            if line.strip() == "":
                break
            parts = line.strip().split()
            atom_id = int(parts[0])
            atom_type = int(parts[1])
            x, y, z = map(float, parts[-3:])
            atoms.append((atom_id, atom_type, x * scale, y * scale, z * scale))

    return [x_bounds, y_bounds, z_bounds], atoms

# ==========================
# Extract Li-ion trajectories (XY projection) from LAMMPS dump
# ==========================
def extract_li_trajectories_xy(dumpfile, scale=1.2, li_type=1):
    with open(dumpfile, 'r') as f:
        lines = f.readlines()

    traj_dict = defaultdict(list)
    i = 0
    while i < len(lines):
        if "ITEM: TIMESTEP" in lines[i]:
            i += 1
        elif "ITEM: NUMBER OF ATOMS" in lines[i]:
            i += 1
        elif "ITEM: BOX BOUNDS" in lines[i]:
            i += 3
        elif "ITEM: ATOMS" in lines[i]:
            headers = lines[i].strip().split()[2:]
            id_index = headers.index('id')
            type_index = headers.index('type')
            x_index = headers.index('x')
            y_index = headers.index('y')
            i += 1
            while i < len(lines) and not lines[i].startswith("ITEM:"):
                parts = lines[i].split()
                if int(parts[type_index]) == li_type:
                    atom_id = int(parts[id_index])
                    x = float(parts[x_index]) * scale
                    y = float(parts[y_index]) * scale
                    traj_dict[atom_id].append((x, y))
                i += 1
        else:
            i += 1
    return traj_dict

# ==========================
# Main plotting function
# ==========================
def plot_structure_and_li_trajectories_xy(data_file, dump_file, output_img):
    scale = 1.0
    box_bounds, atoms = read_lammps_data(data_file, scale=scale)
    traj_dict = extract_li_trajectories_xy(dump_file, scale=scale, li_type=1)

    li_coords = [(x, y) for (_, t, x, y, _) in atoms if t == 1]
    cl_coords = [(x, y) for (_, t, x, y, _) in atoms if t == 2]
    o_coords  = [(x, y) for (_, t, x, y, _) in atoms if t == 3]

    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot Li⁺ trajectories
    for traj in traj_dict.values():
        traj = np.array(traj)
        ax.plot(traj[:, 0], traj[:, 1], color='lightgreen', linewidth=0.7, alpha=0.7, zorder=1)

    # Plot static initial positions
    if li_coords:
        ax.scatter(*zip(*li_coords), c='green', s=120, label='Li$^+$', edgecolors='k', zorder=10)
    if cl_coords:
        ax.scatter(*zip(*cl_coords), c='blue', s=220, label='Cl$^-$', edgecolors='k', zorder=10)
    if o_coords:
        ax.scatter(*zip(*o_coords), c='red', s=180, label='O$^{2-}$', edgecolors='k', zorder=10)

    ax.set_xlabel("X (Å)", fontsize=14)
    ax.set_ylabel("Y (Å)", fontsize=14)
    ax.set_aspect('equal')
    ax.set_title("Li$^+$ Trajectories in XY Plane", fontsize=18)

    # Legend inside upper right
    ax.legend(loc='upper right', fontsize=12, frameon=True)

    plt.tight_layout()
    plt.savefig(output_img, dpi=600)
    plt.show()

# ==========================
# Main entry point
# ==========================
if __name__ == "__main__":
    plot_structure_and_li_trajectories_xy(
        data_file="lammps.data",
        dump_file="traj_all.lammpstrj",
        output_img="Li_XY_fulltrajectory_scaled.png"
    )