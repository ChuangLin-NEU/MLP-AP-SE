import numpy as np
import glob
import re
import matplotlib.pyplot as plt

# ---------- Extract data ----------
temps = []
volumes = []
lengths = []

# Automatically read all thermal_expansion_XXXK.txt files
files = sorted(glob.glob("thermal_expansion_*K.txt"), key=lambda x: int(re.search(r"(\d+)K", x).group(1)))

for fname in files:
    data = np.loadtxt(fname, comments="#")
    temp_avg = np.mean(data[:, 1])   # Temperature
    vol_avg = np.mean(data[:, 2])    # Volume
    lx_avg = np.mean(data[:, 3])     # Lx (assuming cubic cell)

    temps.append(temp_avg)
    volumes.append(vol_avg)
    lengths.append(lx_avg)

temps = np.array(temps)
volumes = np.array(volumes)
lengths = np.array(lengths)

# ---------- Fitting ----------
# Fit Volume vs. Temperature
vol_fit = np.polyfit(temps, volumes, 1)
dVdT = vol_fit[0]
V0 = volumes[0]
alpha_V = dVdT / V0   # Volume thermal expansion coefficient

# Fit Lattice Constant vs. Temperature
len_fit = np.polyfit(temps, lengths, 1)
dLdT = len_fit[0]
L0 = lengths[0]
alpha_L = dLdT / L0   # Linear thermal expansion coefficient

# ---------- Print and save results ----------
print(f" Volume thermal expansion coefficient α_V = {alpha_V:.3e} K^-1")
print(f" Linear thermal expansion coefficient α_L = {alpha_L:.3e} K^-1")

with open("expansion_coefficients.txt", "w") as f:
    f.write("Thermal Expansion Coefficients (from LAMMPS output)\n")
    f.write("-----------------------------------------------------\n")
    f.write(f"Volume thermal expansion coefficient α_V = {alpha_V:.6e} K^-1\n")
    f.write(f"Linear thermal expansion coefficient α_L = {alpha_L:.6e} K^-1\n")
    f.write(f"Fitted V(T): V = {vol_fit[0]:.6f} * T + {vol_fit[1]:.3f}\n")
    f.write(f"Fitted L(T): L = {len_fit[0]:.6f} * T + {len_fit[1]:.3f}\n")

# ---------- Visualization and save figure ----------
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(temps, volumes, 'o-', label='Volume (avg)', color='blue')
plt.plot(temps, np.polyval(vol_fit, temps), '--', label='Linear Fit', color='navy')
plt.xlabel("Temperature (K)")
plt.ylabel("Volume (Å³)")
plt.title("Thermal Expansion (Volume)")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(temps, lengths, 'o-', label='Lattice Const (Lx)', color='green')
plt.plot(temps, np.polyval(len_fit, temps), '--', label='Linear Fit', color='darkgreen')
plt.xlabel("Temperature (K)")
plt.ylabel("Lattice Constant (Å)")
plt.title("Thermal Expansion (Lattice)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("thermal_expansion.png", dpi=300)
plt.show()