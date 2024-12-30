import os
import subprocess

# Define the directory containing the CSV files
input_dir = "NVT_Trajectories"

# List all relevant files
csv_files = [f for f in os.listdir(input_dir) if f.startswith("NVT") and f.endswith("_stress_tensor.csv")]

# Loop through each file and execute viscosityCalculation.py
ct = 1
for csv_file in csv_files:
    if(ct < 32):
        ct += 1
        continue
    input_path = os.path.join(input_dir, csv_file)
    output_dir = os.path.splitext(csv_file)[0] + "_data"  # Create output directory name
    os.makedirs(output_dir, exist_ok=True)

    # Define the command to run the script
    command = [
        "python", "viscosity_calculation.py", input_path,
        "-s", "1000001", "-t", "0.002", "-T", "298", "-v", "141930.7610", "-u", "GPa", "-p"
    ]

    # Run the script
    subprocess.run(command, check=True)
    print(f"Processed: {csv_file}")
