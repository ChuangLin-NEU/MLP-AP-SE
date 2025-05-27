import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# === Step 0: Automatically read LAMMPS box dimensions ===
def get_box_dimensions(data_file):
    with open(data_file, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if "xlo xhi" in lines[i]:
                xlo, xhi = map(float, lines[i].split()[:2])
            if "ylo yhi" in lines[i]:
                ylo, yhi = map(float, lines[i].split()[:2])
            if "zlo zhi" in lines[i]:
                zlo, zhi = map(float, lines[i].split()[:2])
                break
    lx = (xhi - xlo) * 8  # replicated in x-direction
    ly = yhi - ylo
    lz = zhi - zlo
    return lx * 1e-10, ly * 1e-10, lz * 1e-10  # Convert to meters

# === Step 1: Load temperature distribution from temp_profile.dat ===
def load_temperature(filename):
    raw = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip().startswith('#') or line.strip().startswith('ITEM'):
                continue
            parts = line.strip().split()
            if len(parts) >= 4:
                chunk_id = int(parts[0])
                temp = float(parts[3])
                raw.append([chunk_id, temp])
    
    df = pd.DataFrame(raw, columns=["ChunkID", "Temp"])
    grouped = df.groupby("ChunkID").mean().reset_index()
    
    chunk_ids = grouped["ChunkID"].to_numpy()
    temps = grouped["Temp"].to_numpy()
    return chunk_ids, temps

# === Step 1.5: Plot temperature profile ===
def plot_temperature(x, temps):
    plt.figure()
    plt.plot(x, temps, 'o-', label='Temperature profile')
    plt.xlabel('x position (m)')
    plt.ylabel('Temperature (K)')
    plt.title('Temperature Profile from NEMD')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("temp_profile.png", dpi=300)
    plt.show()

# === Step 2: Compute heat flux from heatflow.dat ===
def compute_heat_flux(filename, area):
    data = np.loadtxt(filename, skiprows=1)
    times = data[:, 0]
    EL = data[:, 1]
    ER = data[:, 2]

    N = len(times) // 2
    slope_L, *_ = linregress(times[N:], EL[N:])
    slope_R, *_ = linregress(times[N:], ER[N:])

    J = (slope_L - slope_R) / (2 * area)  # eV/fs/m²
    J *= 1.60218e-19 / 1e-15              # Convert to W/m²
    return J

# === Step 3: Fit linear temperature gradient and compute thermal conductivity ===
def compute_k(x, T, J):
    fit = linregress(x[10:-10], T[10:-10])  # Fit only central region
    dT_dx = fit.slope
    k = J / dT_dx  # W/m·K
    return k, dT_dx

# === Main program ===
if __name__ == "__main__":
    # File paths
    data_file = "lammps.data"
    temp_file = "temp_profile.dat"
    energy_file = "heatflow.dat"

    # Step 0: Read box dimensions
    lx, ly, lz = get_box_dimensions(data_file)
    area = ly * lz
    length_x = lx
    print(f"Box dimensions: Lx = {length_x:.2e} m, Area = {area:.2e} m²")

    # Step 1: Load temperature profile
    chunk_ids, temps = load_temperature(temp_file)
    x_positions = chunk_ids / max(chunk_ids) * length_x

    # Sort for plotting and fitting
    sorted_indices = np.argsort(x_positions)
    x_positions = x_positions[sorted_indices]
    temps = temps[sorted_indices]

    # Save temperature distribution to CSV (e.g., for plotting in Origin)
    data = pd.DataFrame({
        'X_Position': x_positions,
        'Temperature': temps})
    data.to_csv('temperature_distribution.csv', index=False)
    plot_temperature(x_positions, temps)

    # Step 2: Compute heat flux
    J = compute_heat_flux(energy_file, area)
    print(f"Heat flux J = {J:.3e} W/m²")

    # Step 3: Compute thermal conductivity
    k, gradT = compute_k(x_positions, temps, J)
    print(f"Temperature gradient ∂T/∂x = {gradT:.3f} K/m")
    print(f"Thermal conductivity k = {k:.3f} W/m·K")

    # Save results to file
    with open("thermal_conductivity_results.txt", "w") as f:
        f.write(f"Box length (x): {length_x:.5e} m\n")
        f.write(f"Cross-sectional area: {area:.5e} m²\n")
        f.write(f"Heat flux J: {J:.5e} W/m²\n")
        f.write(f"Temperature gradient dT/dx: {gradT:.5f} K/m\n")
        f.write(f"Thermal conductivity k: {k:.5f} W/m·K\n")
    print("Results saved to thermal_conductivity_results.txt")