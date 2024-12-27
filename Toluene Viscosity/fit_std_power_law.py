import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def power_law(t, A, B):
    return A * t**B

inputFile = input("Enter method (Green-Kubo or Einstein): ")
df = pd.read_csv(f"Trajectory_Analysis_CSV_Files/std_{inputFile}.csv")
df = df[df['time(ns)'] > 0]

x = df['time(ns)'].values
y = df['std_visc'].values

popt, pcov = curve_fit(power_law, x, y, p0=(1e-5, 1))
A, B = popt

print("Fitted parameters:")
print("A =", A)
print("B =", B)

plt.figure()
plt.plot(x, y, label="Data", linewidth=1)
plt.plot(x, power_law(x, A, B), color="red", label="Fitted Curve", linewidth=1)
plt.text(0.05, 0.9, f"A={A:.4g}, B={B:.4g}", transform=plt.gca().transAxes, fontsize=10)
plt.xlabel("Time (ns)")
plt.ylabel("Standard Deviation")
plt.legend()
plt.savefig(f"Plots/fitted_std_{inputFile}.png")
plt.close()