from run_fba_usage2 import fba
import numpy as np
from cobra.flux_analysis import flux_variability_analysis
import matplotlib.pyplot as plt

def pe_Data(model, target, objective='curated_biomass', num_points=10):
    """
    Generates the data needed to plot a production envlope between the objective function and a target function across the full range of objective flux values

    Args:
        model (Cobra model): CB model to run simulation on 
        objective (str): desired objective function for simulation. Default is iGR413 LGG model biomass function 'curated_biomass', but could be any model rxn. X-axis on the production envelope 
        target (str): desired target reaction to interrogate. Y-axis on the production envelope
        num_points (int): number of objective value points to be assessed in the FVA range 
    Returns: 
        results (dict): Dictionary of objective value, target value min and max value pairs for plotting
    Notes:
        - Model is constrained previously (example, set_dm must be run first to simulate DM condition)
        - KeyError if objective reaction input does not exist in model 
        - Use  plot_production_envelope to visualize 
        - Cobrapy Version: 0.29.1, Python Version: 3.9.12
    """
    base_fba = fba(model, objective=objective) #Identify max objective flux
    max_bm = float(base_fba.objective_value) 
    bm_values = np.linspace(0, max_bm, num_points) #determine set of objective values to be assessed between 0 and max flux
    results={}
    for b in bm_values:
        mcopy = model.copy()
        mcopy.reactions.get_by_id(objective).bounds = b,b   #constrain objective to specific value
        sol= flux_variability_analysis(mcopy, processes=1)
        target_min=sol.loc[target, 'minimum'] #extract minimum and maximum flux through target at that objective value
        target_max=sol.loc[target, 'maximum']
        results[b]= target_min, target_max 
    return results

def plot_production_envelope_single(results1, label1, save_dir,title,filename, xlab="biomass flux",ylab="target_flux", color_pick="#00000"):
    """
    """
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

    bm_vals = np.array(sorted(results1.keys()))
    maxs = np.array([results1[b][1] for b in bm_vals])
    bm_vals = np.append(bm_vals, bm_vals[-1])
    maxs = np.append(maxs, 0)
    plt.plot(bm_vals, maxs, 'o-', color=color_pick, label=label1, alpha=0.9)
    plt.title(title) 
    plt.xlabel(xlab, fontsize=12)
    plt.ylabel(ylab, fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    directory_name= save_dir + "/" + filename + ".svg"
    plt.savefig(directory_name, format='svg') 
    plt.show()
    plt.close()
