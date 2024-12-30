import os
import pandas as pd
import matplotlib.pyplot as plt

# input method GK or Einstein
method = input("Enter the method (GK or Einstein): ")
# Define the path to the output CSV file
input_csv = f"Trajectory_Analysis_CSV_Files/avg_min_max_visc_{method}.csv"

# Define the output directory for saving the plot
output_plot_dir = "Plots"
os.makedirs(output_plot_dir, exist_ok=True)

# Read the CSV file
data = pd.read_csv(input_csv)

# Extract the "time(ps)" column
time = data["time(ps)"]

# Convert all viscosity columns from Pa·s to mPa·s (multiply by 1000)
for col in data.columns:
    if "viscosity(Pa.s)" in col:
        data[col] = data[col] * 1000

# Filter viscosity columns
viscosity_columns = [col for col in data.columns if "viscosity(Pa.s)" in col]

# Plot all viscosity columns on a single graph
plt.figure(figsize=(16, 12))  # Increased figure size for higher resolution

for col in viscosity_columns:
    if "Average" in col:
        plt.plot(time, data[col], label=col.replace("Pa.s", "mPa.s"), linestyle="--", linewidth=2)
    elif "Minimum" in col:
        plt.plot(time, data[col], label=col.replace("Pa.s", "mPa.s"), linestyle=":", linewidth=2, color="blue")
    elif "Maximum" in col:
        plt.plot(time, data[col], label=col.replace("Pa.s", "mPa.s"), linestyle="-.", linewidth=2, color="red")
    else:
        plt.plot(time, data[col], label=col.replace("Pa.s", "mPa.s"), alpha=0.6)  # Individual viscosities with transparency

# Customize the plot
plt.xlabel("Time (ps)", fontsize=14)
plt.ylabel("Viscosity (mPa.s)", fontsize=14)
plt.title("All Viscosities vs Time (in mPa.s)", fontsize=16)
plt.legend(loc="best", fontsize=10)
plt.grid(True)

# Save the plot
output_plot_path = os.path.join(output_plot_dir, f"visc_trajs_plot_{method}.png")
plt.savefig(output_plot_path, dpi=300)  # Set higher DPI for better resolution
plt.close()

print(f"Plot saved: {output_plot_path}")
