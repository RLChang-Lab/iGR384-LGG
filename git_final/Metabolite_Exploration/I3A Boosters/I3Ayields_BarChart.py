#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:14:26 2026

@author: grichmond
"""

#I3A Yield Bar Chart
import matplotlib.pyplot as plt
import numpy as np

#X-axis: treatment
#y-axis: 90% max BM I3A yield 
#Read in data as key=treatment, value =[Dm52_result, DM24_Result]
data= {"Unsupplemented": [2.76, 1.26],
       "Indole": [3.09, 1.74],
       "Ribose Supplement": [2.60, 1.27],
       "Ribose Replacement": [3.93, 1.57]}

# Extract values
treatments = list(data.keys())
dm52 = np.array([data[t][0] for t in treatments])
dm24 = np.array([data[t][1] for t in treatments])

# Control values
control_52 = dm52[0]
control_24 = dm24[0]

x = np.arange(len(treatments))
width = 0.35

# Final colors
pink = "#6f9a6a"   # DM52
blue = "#5e6aab"   # DM24

fig, ax = plt.subplots(figsize=(8,5))

# Bars
ax.bar(
    x - width/2,
    dm52,
    width,
    label="DM52",
    color=pink)

ax.bar(
    x + width/2,
    dm24,
    width,
    label="DM24",
    color=blue)

# Horizontal reference lines
ax.axhline(
    control_52,
    color=pink,
    linestyle="--",
    linewidth=1.8,
    alpha=0.8,
    label="DM52 Unsup")

ax.axhline(
    control_24,
    color=blue,
    linestyle="--",
    linewidth=1.8,
    alpha=0.8,
    label="DM24 Unsup")

ax.set_xticks(x)
ax.set_xticklabels(treatments, rotation=30, ha="right")
ax.set_ylabel("Simulation Result")
ax.set_xlabel("Treatment")
ax.legend(frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig('I3A_yields.svg') 
plt.show()












