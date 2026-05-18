#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:17:51 2026

@author: grichmond
"""

import cobra
import numpy as np
import matplotlib.pyplot as plt
from set_DM_usage import set_dm 
from run_fba_usage import fba
from PE_utils_usage_single import pe_Data

def calculate_yields(PE_data): 
    result = {}
    
    for biomass, secretion in PE_data.items():
        max_flux = secretion["max_target"]
        
        if biomass == 0:
            point_yield = None  # or float('inf') if you prefer
        else:
            point_yield = max_flux / biomass
        
        result[biomass] = {
            "max_target": max_flux,
            "yield": point_yield
        }
    
    return result

model=cobra.io.read_sbml_model('iGR385.xml')
model_52, media_52= set_dm(model,"52")
unsup_52=pe_Data(model_52, "EX_i3a_e")
unsup_52_Yield=calculate_yields(unsup_52)

model_I= model_52.copy()
model_I.add_boundary(model_52.metabolites.indole_c, type="sink")
model_I.reactions.get_by_id('SK_indole_c').lower_bound= -0.125 #insert here, gotta check
I_data=pe_Data(model_I, "EX_i3a_e")
I_yields=calculate_yields(I_data)

model_R25= model_52.copy()
model_R25.add_boundary(model_52.metabolites.rib__D_c, type="sink")
model_R25.reactions.get_by_id('SK_rib__D_c').lower_bound= -2.5 #insert here, gotta check
R25_data=pe_Data(model_R25, "EX_i3a_e")
R25_yields=calculate_yields(R25_data)

model_R100= model_52.copy()
model_R100.add_boundary(model_52.metabolites.rib__D_c, type="sink")
model_R100.reactions.get_by_id('SK_rib__D_c').lower_bound= -10 #insert here, gotta check
model_R100.reactions.get_by_id("EX_glc__D_e").lower_bound=0
R100_data=pe_Data(model_R100, "EX_i3a_e")
R100_yields=calculate_yields(R100_data)

#######################
model_24, media_25= set_dm(model,"24")
unsup_24=pe_Data(model_24, "EX_i3a_e")
unsup_24_Yield=calculate_yields(unsup_24)

model_I_24= model_24.copy()
model_I_24.add_boundary(model_24.metabolites.indole_c, type="sink")
model_I_24.reactions.get_by_id('SK_indole_c').lower_bound= -0.125 #insert here, gotta check
I_data_24=pe_Data(model_I_24, "EX_i3a_e")
I_24_Yield=calculate_yields(I_data_24)

model_R25_24= model_24.copy()
model_R25_24.add_boundary(model_24.metabolites.rib__D_c, type="sink")
model_R25_24.reactions.get_by_id('SK_rib__D_c').lower_bound= -2.5 #insert here, gotta check
R25_data_24=pe_Data(model_R25_24, "EX_i3a_e")
R25_24_Yield=calculate_yields(R25_data_24)

model_R100_24= model_24.copy()
model_R100_24.add_boundary(model_24.metabolites.rib__D_c, type="sink")
model_R100_24.reactions.get_by_id('SK_rib__D_c').lower_bound= -10 #insert here, gotta check
model_R100_24.reactions.get_by_id("EX_glc__D_e").lower_bound=0
R100_data_24=pe_Data(model_R100_24, "EX_i3a_e")
R100_24_Yield=calculate_yields(R100_data_24)

yield_dict={
    "52_unsup": unsup_52_Yield,
    "52_indole": I_yields,
    "52_Ribose_25": R25_yields,
    "52_Ribose_100": R100_yields,
    "24_unsup": unsup_24_Yield, 
    "24_indole": I_24_Yield, 
    "24_Ribose_25": R25_24_Yield,
    "24_Ribose_100": R100_24_Yield
}

import pandas as pd
def export_yields_to_excel(results_dict, filename="yields.xlsx"):
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        
        for sheet_name, result in results_dict.items():
            
            # Convert nested dict → DataFrame
            df = pd.DataFrame.from_dict(result, orient="index")
            
            # Make biomass a column instead of index
            df.index.name = "biomass_flux"
            df.reset_index(inplace=True)
            
            # Write to sheet (Excel sheet names max length = 31)
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

    print(f"Saved to {filename}")

export_yields_to_excel(yield_dict, "figureC_yields.xlsx")

result_dict={
    "52_unsup": [unsup_52, "#010101"], 
    "52_indole": [I_data, '#7d277d'],
    "52_Ribose_25": [R25_data,'#818181'],
    "52_Ribose_100": [R100_data,'#faa51a'],
    "24_unsup": [unsup_24, "#a0a0a0"], 
    "24_indole": [I_data_24, '#c541c9'],
    "24_Ribose_25": [R25_data_24,'#dddddd'],
    "24_Ribose_100": [R100_data_24,'#f9e65d']}

def big_PE(PE_result_dict, save_dir, title, xlab, ylab, filename):

    os.makedirs(save_dir, exist_ok=True)

    plt.rcParams.update({
        "font.family": "Helvetica",
        "axes.linewidth": 1.2,
        "axes.edgecolor": "gray",
        "grid.color": "lightgray",
        "grid.linestyle": "--",
        "grid.linewidth": 0.8,
        "legend.frameon": False,
    })

    plt.figure(figsize=(8, 6))

    for label, (results, color) in PE_result_dict.items():
        bm_vals = np.array(sorted(results.keys()))
        maxs = np.array([results[b]['max_target'] for b in bm_vals])

        # optional: append final drop to zero
        bm_vals_plot = np.append(bm_vals, bm_vals[-1])
        maxs_plot = np.append(maxs, 0)

        plt.plot(
            bm_vals_plot,
            maxs_plot,
            marker='o',
            linestyle='-',
            color=color,
            label=label,
            alpha=0.9
        )

    plt.title(title)
    plt.xlabel(xlab, fontsize=12)
    plt.ylabel(ylab, fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()

    outpath = os.path.join(save_dir, filename)
    if not outpath.endswith(".svg"):
        outpath += ".svg"

    plt.savefig(outpath, format='svg')
    plt.show()
    plt.close()
    
big_PE(
    result_dict,
    "directory",
    "Checking Growth Coupling",
    "Biomass Flux",
    "I3A Secretion Flux",
    "I3A supplementation"
)