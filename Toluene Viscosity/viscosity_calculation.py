# --------------------------------------------------------------------------------------------

# visco.py is a code for calculating viscosity from molecular dynamics (MD) simulations.
# Copyright (C) 2021 Omid Shayestehpour

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.

# Calculation of viscosity using the Einstein or Green-Kubo expressions.
# Viscosity is computed from the integral of the elements of the pressure tensor
# (or their auto-correlation function) collected from NVT MD simulations.

# Notice: the pressure tensor file should be a CSV file with the following columns 
# (with or without a 'Frame' column) and units of [atm/bar/Pa]:
# Frame (optional), StressXX, StressYY, StressZZ, StressXY, StressXZ, StressYZ

# -------------------------------------------------------------------------------------------

import sys
import argparse
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import integrate
from scipy.constants import Boltzmann
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define Auto-Correlation Function (ACF) using FFT for efficiency
def acf(data):  
    steps = data.shape[0]
    lag = steps//2

    # Nearest size with power of 2 (for efficiency) to zero-pad the input data
    size = 2 ** int(np.ceil(np.log2(2*steps - 1)))
 
    # Compute the FFT
    FFT = np.fft.fft(data, size)

    # Get the power spectrum
    PWR = FFT.conjugate() * FFT

    # Calculate the auto-correlation from inverse FFT of the power spectrum
    COR = np.fft.ifft(PWR)[:steps].real

    autocorrelation = COR / np.arange(steps, 0, -1)

    return autocorrelation[:lag]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parser():
    parser = argparse.ArgumentParser(
        prog="visco.py",
        description='Calculation of viscosity from (NVT) molecular dynamics simulations.'
    )

    parser.add_argument(
        'datafile', 
        help='Path to the pressure tensor CSV data file. \
        The CSV should contain columns: Frame (optional), StressXX, StressYY, StressZZ, StressXY, StressXZ, StressYZ.'
    )

    parser.add_argument(
        '-u', '--unit', choices=['Pa', 'atm', 'bar', 'GPa'], default='atm', 
        help='Unit of the provided pressure data: Pa, atm, bar, or GPa. Default is atm.'
    )

    parser.add_argument(
        '-s', '--steps', type=int, required=True, 
        help='Number of steps (rows) to read from the pressure tensor file.'
    )

    parser.add_argument(
        '-t', '--timestep', type=float, required=True, 
        help='Physical timestep between two successive pressure data points in [ps].'
    )

    parser.add_argument(
        '-T', '--temperature', type=float, required=True, 
        help='Temperature of the MD simulation in [K].'
    )

    parser.add_argument(
        '-v', '--volume', type=float, required=True, 
        help='Volume of the simulation box in [A^3] (Angstorm cube).'
    )

    parser.add_argument(
        '-d', '--diag', action='store_false',  
        help='Exclude diagonal elements of the pressure tensor for viscosity calculation using Green-Kubo approach. \
        By default, diagonal elements are included.'
    )

    parser.add_argument(
        '-p', '--plot', action='store_true',  
        help='Show plots of auto-correlation functions and running integral of viscosity.'
    )

    parser.add_argument(
        '-e', '--each', type=int, default=100, 
        help='Interval of steps to save the time evolution of viscosity. Default is 100.'
    )

    args = parser.parse_args()

    # Check if the file exists
    try:
        with open(args.datafile, "r") as file:
            pass
    except IOError as error:
        print(f'Error: {error}')
        sys.exit(1)

    return args

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Viscosity from Einstein relation
def einstein():
    Pxxyy = (Pxx - Pyy) / 2
    Pyyzz = (Pyy - Pzz) / 2

    '''
    Calculate the viscosity from the Einstein relation 
    by integrating the components of the pressure tensor
    '''
    timestep_sec = args.timestep * 1e-12  # Convert ps to seconds

    # Perform cumulative integration using the trapezoidal rule
    Pxy_int = integrate.cumulative_trapezoid(y=Pxy, dx=timestep_sec, initial=0)
    Pxz_int = integrate.cumulative_trapezoid(y=Pxz, dx=timestep_sec, initial=0)
    Pyz_int = integrate.cumulative_trapezoid(y=Pyz, dx=timestep_sec, initial=0)
    Pxxyy_int = integrate.cumulative_trapezoid(y=Pxxyy, dx=timestep_sec, initial=0)
    Pyyzz_int = integrate.cumulative_trapezoid(y=Pyyzz, dx=timestep_sec, initial=0)

    # Compute the integral as per Einstein relation
    integral = (Pxy_int**2 + Pxz_int**2 + Pyz_int**2 + Pxxyy_int**2 + Pyyzz_int**2) / 5

    # Avoid division by zero by ensuring Time[1:] is non-zero
    viscosity = integral[1:] * (args.volume * 1e-30) / (2 * kBT * Time[1:] * 1e-12)

    return viscosity

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Viscosity from Green-Kubo relation
def green_kubo():
    # Calculate the ACFs
    Pxy_acf = acf(Pxy)
    Pxz_acf = acf(Pxz)
    Pyz_acf = acf(Pyz)

    # Calculate the shear components of the pressure tensor and their ACF
    if args.diag:
        Pxxyy = (Pxx - Pyy) / 2
        Pyyzz = (Pyy - Pzz) / 2
        Pxxzz = (Pxx - Pzz) / 2

        Pxxyy_acf = acf(Pxxyy)
        Pyyzz_acf = acf(Pyyzz)
        Pxxzz_acf = acf(Pxxzz)

    # Compute the average ACF
    if args.diag:
        avg_acf = (Pxy_acf + Pxz_acf + Pyz_acf + Pxxyy_acf + Pyyzz_acf + Pxxzz_acf) / 6
    else:
        avg_acf = (Pxy_acf + Pxz_acf + Pyz_acf) / 3

    # Integrate the average ACF to get the viscosity
    timestep_sec = args.timestep * 1e-12  # Convert ps to seconds
    integral = integrate.cumulative_trapezoid(y=avg_acf, dx=timestep_sec, initial=0)
    viscosity_gk = integral * (args.volume * 1e-30) / kBT
    return avg_acf, viscosity_gk
args = parser()

# Conversion ratio from atm/bar/GPa to Pa
conversion_factors = {
    'Pa': 1,
    'atm': 101325,
    'bar': 100000,
    'GPa': 1e9
}

conv_ratio = conversion_factors.get(args.unit, 1)

# Calculate the kBT value
kBT = Boltzmann * args.temperature

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read the pressure tensor elements from CSV file using Pandas
print('\nReading the pressure tensor data file with Pandas')

try:
    # Read the CSV file, assuming it may have a header. Read only the specified number of steps.
    # Skip malformed lines by setting on_bad_lines to 'skip'
    df = pd.read_csv(args.datafile, nrows=args.steps, on_bad_lines='skip')
except TypeError:
    # For older versions of pandas that don't have on_bad_lines
    df = pd.read_csv(args.datafile, nrows=args.steps, error_bad_lines=False, warn_bad_lines=True)
except Exception as e:
    print(f"Error reading the data file with Pandas: {e}")
    sys.exit(1)

# Check if 'Frame' column exists and drop it if present
if 'Frame' in df.columns:
    df = df.drop(columns=['Frame'])

# Define expected columns based on your CSV
expected_columns = ['StressXX', 'StressYY', 'StressZZ', 'StressXY', 'StressXZ', 'StressYZ']

# Ensure that all expected columns are present
if not all(col in df.columns for col in expected_columns):
    print(f"Error: CSV file must contain the following columns: {expected_columns}")
    sys.exit(1)

# Select only the required columns
df = df[expected_columns]

# Check for missing values
if df.isnull().values.any():
    print("Error: CSV file contains missing values. Please clean the data before proceeding.")
    sys.exit(1)

# Rename columns to match internal variable names
df.rename(columns={
    'StressXX': 'Pxx',
    'StressYY': 'Pyy',
    'StressZZ': 'Pzz',
    'StressXY': 'Pxy',
    'StressXZ': 'Pxz',
    'StressYZ': 'Pyz'
}, inplace=True)

# Convert to float and apply unit conversion
try:
    df = df.astype(float) * conv_ratio
except ValueError:
    print("Error: Non-numeric values found in the data file.")
    sys.exit(1)

# Assign to respective variables as NumPy arrays
Pxx = df['Pxx'].values
Pyy = df['Pyy'].values
Pzz = df['Pzz'].values
Pxy = df['Pxy'].values
Pxz = df['Pxz'].values
Pyz = df['Pyz'].values

print(f"Number of data points read: {len(Pxx)}")
if len(Pxx) == 0:
    print("Error: No data was read from the input file.")
    sys.exit(1)

# Generate the time array based on actual data points read
end_time_ps = len(Pxx) * args.timestep
print(f"Total simulation time: {end_time_ps} ps")
Time = np.linspace(0, end_time_ps, num=len(Pxx), endpoint=False)

viscosity_einstein = einstein()

# Create output directory based on the input file name
base_filename = os.path.splitext(os.path.basename(args.datafile))[0]  # Extract base name
output_dir = f"{base_filename}_data"  # Define output directory name
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

print(f"\nViscosity (Einstein): {round((viscosity_einstein[-1] * 1000), 2)} [mPa.s]")

# Plot the running integral of viscosity
if args.plot:
    plt.figure(figsize=(8,6))
    plt.plot(Time[:len(viscosity_einstein)], viscosity_einstein * 1000, label='Viscosity (Einstein)')
    plt.xlabel('Time (ps)')
    plt.ylabel('Viscosity (mPa.s)')
    plt.title('Viscosity (Einstein) vs Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "viscosity_Einstein.png"))
    # plt.show()




# Save the running integral of viscosity as a CSV file
df_einstein = pd.DataFrame({
    "time(ps)": Time[:len(viscosity_einstein):args.each],
    "viscosity(Pa.s)": viscosity_einstein[::args.each]
})
df_einstein.to_csv(os.path.join(output_dir, "viscosity_Einstein.csv"), index=False)


# df_einstein.to_csv("viscosity_Einstein.csv", index=False)


avg_acf, viscosity_gk = green_kubo()

# Plot the normalized average ACF
if args.plot:
    norm_avg_acf = avg_acf / avg_acf[0]
    plt.figure(figsize=(8,6))
    plt.plot(Time[:len(norm_avg_acf)], norm_avg_acf, label='Normalized ACF (Green-Kubo)')
    plt.xlabel('Time (ps)')
    plt.ylabel('Normalized ACF')
    plt.title('Auto-Correlation Function (Green-Kubo) vs Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "acf_plot.png"))
    # plt.show()
    


# Save the normalized average ACF as a CSV file
norm_avg_acf = avg_acf / avg_acf[0]
df_acf = pd.DataFrame({
    "time(ps)": Time[:len(norm_avg_acf)],
    "ACF": norm_avg_acf
})
# df_acf.to_csv("avg_acf.csv", index=False)
df_acf.to_csv(os.path.join(output_dir, "avg_acf.csv"), index=False)


print(f"Viscosity (Green-Kubo): {round((viscosity_gk[-1] * 1000), 2)} [mPa.s]")
print("Note: Do not trust these values! You should fit an exponential function to the running integral and take its limit.")

# Plot the time evolution of the viscosity estimate
if args.plot:
    plt.figure(figsize=(8,6))
    plt.plot(Time[:len(viscosity_gk)], viscosity_gk * 1000, label='Viscosity (Green-Kubo)')
    plt.xlabel('Time (ps)')
    plt.ylabel('Viscosity (mPa.s)')
    plt.title('Viscosity (Green-Kubo) vs Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "viscosity_GK.png"))
    # plt.show()


# Save running integral of the viscosity as a CSV file
df_gk = pd.DataFrame({
    "time(ps)": Time[:len(viscosity_gk):args.each],  # Actual time points
    "viscosity(Pa.s)": viscosity_gk[::args.each]    # Corresponding viscosity values
})
df_gk.to_csv(os.path.join(output_dir, "viscosity_GK.csv"), index=False)
