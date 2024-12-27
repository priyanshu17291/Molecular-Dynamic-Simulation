import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def double_exponential(t, A, a, T1, T2):
    return A*a*T1*(1 - np.exp(-t / T1)) + A*(1 - a)*T2*(1 - np.exp(-t / T2))

inputFile = input("Enter method (Green-Kubo or Einstein): ")
t_cut = int(input("Enter t_cut row number: "))
data = pd.read_csv(f"Trajectory_Analysis_CSV_Files/std_{inputFile}.csv")

# Select only the first 1661 rows for fitting
data_subset = data.iloc[:t_cut]
time = data_subset["time(ns)"].values
visc = data_subset["mean_visc"].values

initial_guess = [0.0003, 0.5, 0.001, 0.001]
params, _ = curve_fit(double_exponential, time, visc, p0=initial_guess)

print("Fitted parameters:")
print(f"A = {params[0]}")
print(f"a = {params[1]}")
print(f"T1 = {params[2]}")
print(f"T2 = {params[3]}")

plt.plot(time, visc*1000, label="Data", linewidth=1)
plt.plot(time, double_exponential(time, *params) * 1000, color="red", label="Fitted Curve", linewidth=1)
plt.text(0.05, 0.9, f"A={params[0]:.4g}, a={params[1]:.4g}, T1={params[2]:.4g}, T2={params[3]:.4g}", transform=plt.gca().transAxes, fontsize=10)
plt.xlabel("Time (ns)")
plt.ylabel("Mean Viscosity (mPa.s)")
plt.legend()
plt.savefig(f"plots/fitted_avgvisc_{inputFile}.png")
plt.close()