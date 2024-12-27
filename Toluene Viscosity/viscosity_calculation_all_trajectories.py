import os
import subprocess

# Define the directory containing the CSV files
input_dir = "C:/Users/priya/WinterProject/Green_Kubo/All_Stress_Tensor_csv/AllStressTensorFiles"

# List all relevant files
csv_files = [f for f in os.listdir(input_dir) if f.startswith("NVT") and f.endswith("_stress_tensor.csv")]

# Loop through each file and execute viscosityCalculation.py
for csv_file in csv_files:
    input_path = os.path.join(input_dir, csv_file)
    output_dir = os.path.splitext(csv_file)[0] + "_data"  # Create output directory name
    os.makedirs(output_dir, exist_ok=True)

    # Define the command to run the script
    command = [
        "python", "viscosityCalculation.py", input_path,
        "-s", "1000001", "-t", "0.002", "-T", "298", "-v", "141930.7610", "-u", "GPa", "-p"
    ]

    # Run the script
    subprocess.run(command, check=True)
    print(f"Processed: {csv_file}")
command2 = ["python","averageViscosityGK.py"]
command3 = ["python","averageViscosityEinstein.py"]
command4 = ["python","plotViscosityTrajectoryGK.py"]
command5 = ["python","plotViscosityTrajectoryEinstein.py"]
subprocess.run(command2)
print("Average Viscosity GK calculated")
subprocess.run(command3)
print("Average Viscosity Einstein calculated")
subprocess.run(command4)
print("Plotting Viscosity Trajectory GK")
subprocess.run(command5)
print("Plotting Viscosity Trajectory Einstein")
