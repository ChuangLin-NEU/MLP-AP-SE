import pandas as pd
import matplotlib.pyplot as plt

# Set global font to Times New Roman for all plots
plt.rcParams['font.family'] = 'Times New Roman'

# Font size configuration
title_fontsize = 18
label_fontsize = 14
legend_fontsize = 12

# === Load training log ===
file_path = "./lcurve.out"  # Replace with your actual path
columns = ['step', 'rmse_val', 'rmse_trn', 'rmse_e_val', 'rmse_e_trn', 
           'rmse_f_val', 'rmse_f_trn', 'rmse_v_val', 'rmse_v_trn', 'lr']
df = pd.read_csv(file_path, delim_whitespace=True, comment='#', names=columns)

# === 1. Plot total RMSE (training vs validation) ===
plt.figure(figsize=(10, 6))
plt.plot(df["step"], df["rmse_val"], label="Validation RMSE", linestyle='-', marker='.')
plt.plot(df["step"], df["rmse_trn"], label="Training RMSE", linestyle='-', marker='.')
plt.xlabel("Step", fontsize=label_fontsize)
plt.ylabel("Total RMSE", fontsize=label_fontsize)
plt.title("Total RMSE Evolution During Training", fontsize=title_fontsize)
plt.legend(fontsize=legend_fontsize)
plt.grid()
plt.savefig("total_rmse_evolution.png", dpi=300)
plt.close()

# === 2. Plot energy RMSE ===
plt.figure(figsize=(10, 6))
plt.plot(df["step"], df["rmse_e_val"], label="Validation Energy RMSE", linestyle='-', marker='.')
plt.plot(df["step"], df["rmse_e_trn"], label="Training Energy RMSE", linestyle='-', marker='.')
plt.xlabel("Step", fontsize=label_fontsize)
plt.ylabel("Energy RMSE", fontsize=label_fontsize)
plt.title("Energy RMSE Evolution During Training", fontsize=title_fontsize)
plt.legend(fontsize=legend_fontsize)
plt.grid()
plt.savefig("energy_rmse_evolution.png", dpi=300)
plt.close()

# === 3. Plot force RMSE ===
plt.figure(figsize=(10, 6))
plt.plot(df["step"], df["rmse_f_val"], label="Validation Force RMSE", linestyle='-', marker='.')
plt.plot(df["step"], df["rmse_f_trn"], label="Training Force RMSE", linestyle='-', marker='.')
plt.xlabel("Step", fontsize=label_fontsize)
plt.ylabel("Force RMSE", fontsize=label_fontsize)
plt.title("Force RMSE Evolution During Training", fontsize=title_fontsize)
plt.legend(fontsize=legend_fontsize)
plt.grid()
plt.savefig("force_rmse_evolution.png", dpi=300)
plt.close()

# === 4. Plot virial RMSE (stress-related) ===
plt.figure(figsize=(10, 6))
plt.plot(df["step"], df["rmse_v_val"], label="Validation Virial RMSE", linestyle='-', marker='.')
plt.plot(df["step"], df["rmse_v_trn"], label="Training Virial RMSE", linestyle='-', marker='.')
plt.xlabel("Step", fontsize=label_fontsize)
plt.ylabel("Virial RMSE", fontsize=label_fontsize)
plt.title("Virial RMSE Evolution During Training", fontsize=title_fontsize)
plt.legend(fontsize=legend_fontsize)
plt.grid()
plt.savefig("virial_rmse_evolution.png", dpi=300)
plt.close()

# === 5. Plot learning rate evolution (log scale) ===
plt.figure(figsize=(10, 6))
plt.plot(df["step"], df["lr"], label="Learning Rate", linestyle='-', marker='.')
plt.xlabel("Step", fontsize=label_fontsize)
plt.ylabel("Learning Rate", fontsize=label_fontsize)
plt.yscale("log")
plt.title("Learning Rate Evolution During Training", fontsize=title_fontsize)
plt.legend(fontsize=legend_fontsize)
plt.grid()
plt.savefig("learning_rate_evolution.png", dpi=300)
plt.close()

# === 6. Plot all RMSE metrics in one log-scale plot ===
plt.figure(figsize=(12, 8))
plt.plot(df["step"], df["rmse_val"], label="Validation Total RMSE", marker='.')
plt.plot(df["step"], df["rmse_trn"], label="Training Total RMSE", marker='.')
plt.plot(df["step"], df["rmse_e_val"], label="Validation Energy RMSE", marker='.')
plt.plot(df["step"], df["rmse_e_trn"], label="Training Energy RMSE", marker='.')
plt.plot(df["step"], df["rmse_f_val"], label="Validation Force RMSE", marker='.')
plt.plot(df["step"], df["rmse_f_trn"], label="Training Force RMSE", marker='.')
plt.plot(df["step"], df["rmse_v_val"], label="Validation Virial RMSE", marker='.')
plt.plot(df["step"], df["rmse_v_trn"], label="Training Virial RMSE", marker='.')
plt.xlabel("Step", fontsize=label_fontsize)
plt.ylabel("RMSE Values (log scale)", fontsize=label_fontsize)
plt.yscale("log")
plt.title("All RMSE Metrics Evolution During Training", fontsize=title_fontsize)
plt.legend(fontsize=legend_fontsize, loc='upper right')
plt.grid()
plt.savefig("all_rmse_metrics_evolution_log.png", dpi=300)
plt.close()