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

# Convert Average, Minimum, and Maximum viscosity columns from Pa·s to mPa·s
data["Average Viscosity (mPa.s)"] = data["Average Viscosity (Pa.s)"] * 1000
data["Minimum Viscosity (mPa.s)"] = data["Minimum Viscosity (Pa.s)"] * 1000
data["Maximum Viscosity (mPa.s)"] = data["Maximum Viscosity (Pa.s)"] * 1000

# Plot Average, Minimum, and Maximum viscosity columns
plt.figure(figsize=(12, 8))

# Fill the area between Minimum and Maximum viscosities with light yellow
plt.fill_between(
    time,
    data["Minimum Viscosity (mPa.s)"],
    data["Maximum Viscosity (mPa.s)"],
    color="lightblue",
    label="Range (Min-Max)"
)

# Plot the Average Viscosity line in royal blue
plt.plot(time, data["Average Viscosity (mPa.s)"], label="Average Viscosity", color="royalblue", linewidth=2)

# Customize the plot
plt.xlabel("Time (ps)", fontsize=14)
plt.ylabel("Viscosity (mPa.s)", fontsize=14)
plt.title("Average, Min, and Max Viscosity vs Time (in mPa.s)", fontsize=16)
plt.legend(loc="best", fontsize=12)
plt.grid(True)

# Save the plot
output_plot_path = os.path.join(output_plot_dir, f"avg_min_max_visc_{method}.png")
plt.savefig(output_plot_path)
plt.close()

print(f"Plot saved: {output_plot_path}")
