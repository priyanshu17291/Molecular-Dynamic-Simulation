import pandas as pd

method = input("Enter the method (Green-Kubo or Einstein): ")
# Path to the CSV file
file_path = f"Trajectory_Analysis_CSV_Files/std_{method}.csv"

# Read the CSV file
df = pd.read_csv(file_path)

# Calculate 40% of mean_visc
threshold = 0.4 * df['mean_visc']

# Iterate through the DataFrame starting from the first non-zero mean_visc
for idx, row in df.iterrows():
    if(idx < 2):
        continue
    if row['mean_visc'] > 0 and row['std_visc'] >= 0.4 * row['mean_visc']:
        print(f"Row {idx} exceeds 40% threshold at time {row['time(ns)']} ns.")
        break
else:
    print("No time point where std_visc reaches 40% of mean_visc.")
