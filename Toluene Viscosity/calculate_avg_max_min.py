import os
import pandas as pd

# Define the working directory containing the 20 subdirectories
working_dir = "Viscosity_Data" # Add the path to your working directory here
# choose data set GK or Einstein
method = input("Enter the method (GK or Einstein): ")

# Initialize an empty list to store data from all files
data_frames = []
directory_names = []  # To track directory names for column headers

# Loop through each subdirectory
for subdir in os.listdir(working_dir):
    subdir_path = os.path.join(working_dir, subdir)

    # Check if the subdir is a directory
    if os.path.isdir(subdir_path):
        viscosity_file = os.path.join(subdir_path, f"viscosity_{method}.csv")
        
        # Check if viscosity_GK.csv exists in the directory
        if os.path.exists(viscosity_file):
            # Read the CSV file
            try:
                df = pd.read_csv(viscosity_file)
                data_frames.append(df)
                directory_names.append(subdir)  # Add directory name for reference
            except Exception as e:
                print(f"Error reading {viscosity_file}: {e}")

# Check if we have any data
if not data_frames:
    print(f"No viscosity_{method}.csv files found!")
    exit()

# Concatenate all data frames row-wise and align by rows based on the "time(ps)" column
aligned_data = pd.concat(
    [df.set_index("time(ps)") for df in data_frames],
    axis=1,
    keys=directory_names
)

# Flatten the multi-level column headers and reset the index
aligned_data.columns = [f"{col[1]} ({col[0]})" for col in aligned_data.columns.to_flat_index()]
aligned_data.reset_index(inplace=True)

# Calculate the mean, minimum, and maximum viscosity values across all directories for each row
aligned_data["Average Viscosity (Pa.s)"] = aligned_data.filter(like="viscosity(Pa.s)").mean(axis=1)
aligned_data["Minimum Viscosity (Pa.s)"] = aligned_data.filter(like="viscosity(Pa.s)").min(axis=1)
aligned_data["Maximum Viscosity (Pa.s)"] = aligned_data.filter(like="viscosity(Pa.s)").max(axis=1)

# Save the results to a new CSV file
output_file = os.path.join("Trajectory_Analysis_CSV_Files", f"avg_min_max_visc_{method}.csv")
aligned_data.to_csv(output_file, index=False)

print(f"Summary CSV created: {output_file}")
