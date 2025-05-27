import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from scipy.optimize import curve_fit

# ------------------------ Read POSCAR for volume and Li count ----------------------------
def read_poscar(poscar_path='POSCAR'):
    with open(poscar_path, 'r') as f:
        lines = f.readlines()

    scale = float(lines[1].strip())
    lattice = np.array([
        list(map(float, lines[2].split())),
        list(map(float, lines[3].split())),
        list(map(float, lines[4].split())),
    ])
    lattice *= scale

    volume = abs(np.linalg.det(lattice))  # Supercell volume in Å³

    elements = lines[5].split()
    numbers = list(map(int, lines[6].split()))

    if 'Li' in elements:
        li_index = elements.index('Li')
        li_count = numbers[li_index]
    else:
        raise ValueError('Li element not found in POSCAR.')

    return volume, li_count

# ------------------------ Physical constants ----------------------------
kB = constants.Boltzmann  # J/K
e_charge = constants.e     # C

# ------------------------ Parameters ----------------------------
T = 600  # Temperature in K
poscar_volume_A3, ion_num = read_poscar('POSCAR')  # Get supercell volume and Li count
cell_volume_cm3 = poscar_volume_A3 * 1e-24  # Convert Å³ to cm³

# Ionic concentration (ions/cm³)
c_ion_cm3 = ion_num / cell_volume_cm3
print(f"Ionic concentration c_ion_cm3 = {c_ion_cm3:.3e} ions/cm³")

# ------------------------ Load MSD data ----------------------------
data = np.loadtxt('msd_Li.out', comments='#')
time_steps_raw = data[:, 0]
time_step_zero = time_steps_raw[0]
relative_time_fs = time_steps_raw - time_step_zero  # Set first step as t=0
relative_time_ps = relative_time_fs * 1e-3          # Convert to ps
msd_A2 = data[:, 1]                                 # MSD in Å²

# ------------------------ Auto fit range ----------------------------
fit_start = int(data[0, 0])
fit_end = int(data[-1, 0])

mask = (data[:, 0] >= fit_start) & (data[:, 0] <= fit_end)
fit_time_s = relative_time_fs[mask] * 1e-15  # Convert to seconds
fit_msd_m2 = msd_A2[mask] * 1e-20            # Convert to m²

# ------------------------ Linear fit for diffusivity ----------------------------
def linear_func(x, a, b):
    return a * x + b

popt, _ = curve_fit(linear_func, fit_time_s, fit_msd_m2)
slope = popt[0]
D_m2_s = slope / 6  # Einstein relation: D = slope / 6
D_cm2_s = D_m2_s * 1e4  # Convert to cm²/s

# ------------------------ Nernst-Einstein conductivity ----------------------------
sigma_S_cm = (D_cm2_s * e_charge**2 * c_ion_cm3) / (kB * T)  # in S/cm

# ------------------------ Plot MSD and fit ----------------------------
plt.rcParams['font.family'] = 'Times New Roman'
plt.figure(figsize=(8,6))
plt.plot(relative_time_ps, msd_A2, label='MSD data', lw=2)
fit_line_ps = fit_time_s * 1e12  # Convert s → ps for plotting
plt.plot(fit_line_ps, linear_func(fit_time_s, *popt) * 1e20, 'r--', label='Linear fit')

plt.xlabel('Time (ps)', fontsize=14)
plt.ylabel(r'MSD ($\mathrm{\AA}^2$)', fontsize=14)
plt.title('Li MSD and Diffusion Fitting', fontsize=16)
plt.legend(fontsize=14)

# Annotate diffusivity and conductivity
textstr = f'Diffusivity = {D_cm2_s:.3e} cm²/s\nConductivity = {sigma_S_cm:.3e} S/cm'
plt.text(0.05 * max(relative_time_ps), 0.15 * max(msd_A2), textstr,
         fontsize=13, bbox=dict(facecolor='white', alpha=0.7))

plt.grid(True)
plt.tight_layout()
plt.savefig('msd_fit.png', dpi=300)
plt.show()

# ------------------------ Print results ----------------------------
print(f"Volume from POSCAR: V = {poscar_volume_A3:.3f} Å³")
print(f"Number of Li atoms = {ion_num}")
print(f"Ionic concentration c_ion_cm3 = {c_ion_cm3:.3e} ions/cm³")
print(f"Fitting range: {fit_start} - {fit_end} steps")
print(f"Diffusivity D = {D_cm2_s:.3e} cm²/s")
print(f"Ionic conductivity σ = {sigma_S_cm:.3e} S/cm")