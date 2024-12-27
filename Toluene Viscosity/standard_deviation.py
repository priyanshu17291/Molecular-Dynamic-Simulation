import os
import pandas as pd

# input method Green-Kubo or Einstein
method = input("Enter the method (Green-Kubo or Einstein): ")
working_dir = "Trajectory_Analysis_CSV_Files"

file_path = os.path.join(working_dir, f"avg_min_max_visc_{method}.csv")
df = pd.read_csv(file_path)

cols = [c for c in df.columns if "viscosity(Pa.s)" in c and "NVT" in c]
df["time(ns)"] = df["time(ps)"] / 1000
df["mean_visc"] = df[cols].mean(axis=1)
df["std_visc"] = df[cols].std(axis=1)

output_file = os.path.join(working_dir, f"std_{method}.csv")
df[["time(ns)", "mean_visc", "std_visc"]].to_csv(output_file, index=False)
import matplotlib.pyplot as plt

plots_dir = os.path.join("Plots")
os.makedirs(plots_dir, exist_ok=True)

data = pd.read_csv(output_file)
plt.figure()
plt.plot(data["time(ns)"], data["std_visc"], label="Std Viscosity")
plt.xlabel("Time (ns)")
plt.ylabel("Standard Deviation (Pa.s)")
plt.title("Std vs Time")
plt.legend()
plt.savefig(os.path.join(plots_dir, f"std_{method}.png"))
plt.close()
