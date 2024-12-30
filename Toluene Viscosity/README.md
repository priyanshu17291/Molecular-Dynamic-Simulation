# Prologue
This repository will help you to know **step by step** process for calculating **Viscosity** of any System using **Materials Studio** software, in this example we are calculating **Viscosity** for Toluene System.

---
## Here is the Step by Step Procedure

**1.** First we requiring **Stress Tensor Data** files for **Toluene** system. (*given below in the **Trajectory Files** section*)

***Note:** For knowing step by step procedure of generating *Stress Tensor Files* see **Additional Resources** section*

**2.** Save all **trajectory files** in one directory *namely* **NVT_Trajectories** and keep all python files present in **Toluene Viscosity** directory and **NVT_Trajectories** in same directory.

*Name and description of each python files is given in **Source Code** Section*

**4.** Run python files in given below order :

    1. generate_visc_data_all_files.py
    2. calculate_avg_max_min.py
**5.** Now for plotting graphs you have use these files:

    plot_visc_trajs.py
    plot_avg_max_min_visc.py
    standard_deviation.py
**6.** For know final viscosity after double exponant fitting, run these files:

    t_cut.py
    double_exp_fit_avgvisc.py



___

## Source code

|Files|Description|
|--------|--------|
|generate_visc_data_all_files.py| For generating Viscosity Data files of all trajectories|
|calculate_avg_max_min.py|Calculating mean, maximum and minimum of Viscosity of all trajectories and store them into a seperate csv file|
|plot_visc_trajs.py|Plots Viscosity vs Time of all trajectories in one graph|
|    plot_avg_max_min_visc.py|Plot average, maxima and minima of viscosity vs time off all trajectories|
|    standard_deviation.py|Calculates Standard Deviation of all trajectories with time and saves in a csv file|
|    t_cut.py| For finding *cut* time *<sub>\*</sub> see Litrature section to know about t<sub>cut</sub>*
|    fit_std_power_law.py|For Power law fitting of Standard Deviation|
|    double_exp_fit_avgvisc.py| For Double Exponant fitting of average viscosity|

---
---


## 📁 Trajectory File

You can download the **trajectory files** directly using the link below:

<a href="https://csciitd-my.sharepoint.com/:f:/g/personal/ch1221465_iitd_ac_in/EvSWEVYWOmBPv91TLEd67usB1UzTbYdoceb69zjKFuTcWQ?e=g441mY" target="_blank" rel="noopener noreferrer">Download Trajectory Files</a>

---


## 📂 Additional Resources

| Resource        | Description                     | Link                                                                                                                      |
|-----------------|---------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Documentation   | Detailed project guides         | <a href="https://csciitd-my.sharepoint.com/:f:/g/personal/ch1221465_iitd_ac_in/EsucStwHih5CgI6IiCgBsM0B9Z2gx2SFuRfBHkqb3AJaXw?e=HrhhHh" target="_blank" rel="noopener noreferrer">View Literature here</a> |
| Source Code     | Complete source code repository | <a href="https://github.com/your-repo" target="_blank" rel="noopener noreferrer">View on GitHub</a>                      |
| Issue Tracker   | Report and track issues         | <a href="https://github.com/your-repo/issues" target="_blank" rel="noopener noreferrer">GitHub Issues</a>                |
