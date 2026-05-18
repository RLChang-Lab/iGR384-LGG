#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:53:17 2026

@author: grichmond
"""
import sys
import cobra
import pandas as pd
from set_DM_usage import set_dm
from run_fba_usage import fba

from cobra import Reaction

def add_atp_free_biomass(model):
    if "curated_bm_noATP" in model.reactions:
        return model

    rxn = Reaction("curated_bm_noATP")
    rxn.name = "Biomass decoupled from ATP"
    rxn.lower_bound = 0
    rxn.upper_bound = 1000

    rxn.add_metabolites({
        model.metabolites.M8801_c: -0.059,
        model.metabolites.M8807_c: -0.087,
        model.metabolites.M8811_c: -0.081,
        model.metabolites.e_Cofactor_c: -0.026,
        model.metabolites.e_DNA_c: -0.063,
        model.metabolites.e_Lipid_c: -0.079,
        model.metabolites.e_Protein_c: -0.308,
        model.metabolites.e_RNA_c: -0.297,
        model.metabolites.e_Biomass_c: 1,
    })

    model.add_reactions([rxn])
    return model

def prepare_atp_model(model):
    model = model.copy()

    
    # Remove original biomass
    if "curated_biomass" in model.reactions:
        model.remove_reactions(["curated_biomass"])
    # Block lactate production routes
    for i in model.metabolites.lac__L_c.reactions:
        i.bounds = (0, 0)
    # Set ATP maintenance as objective
    model.objective = "ATPM"

    return model

######################################################
if __name__ == "__main__":
    model = cobra.io.read_sbml_model('iGR385.xml')
    
    model = add_atp_free_biomass(model)

    # Disable original biomass, but keep ATP-free biomass available
    if "curated_biomass" in model.reactions:
        model.reactions.curated_biomass.bounds = (0, 0)

    # Inhibit lactate
    for rxn in model.metabolites.lac__L_c.reactions:
        if rxn in model.reactions:
            rxn.bounds = (0, 0)

    model.objective = "ATPM"
    
    test_medias=['52', '24']
    for i in test_medias:
        model2 = model.copy()
        model_set, media_set = set_dm(model2, i)
    
        model_set.objective = "ATPM"
    
        # Optional: require biomass precursors to remain producible
        model_set.reactions.curated_bm_noATP.lower_bound = 1e-6
    
        solution = cobra.flux_analysis.parsimonious.pfba(model_set)
    
        fluxes = solution.fluxes
        ATP_RELATED_METS = {"atp_c", "adp_c", "amp_c", "pi_c", "ppi_c"}

        rows = []
        
        for rxn_id, flux in fluxes.items():
            if abs(flux) <= 1e-9:
                continue
        
            rxn = model_set.reactions.get_by_id(rxn_id)
        
            met_ids = {met.id for met in rxn.metabolites}
        
            if not met_ids.intersection(ATP_RELATED_METS):
                continue
        
            rows.append({
                "reaction_id": rxn.id,
                "reaction_name": rxn.name,
                "formula": rxn.reaction,
                "flux": flux,
                "lower_bound": rxn.lower_bound,
                "upper_bound": rxn.upper_bound
            })
        
        rxn_df = pd.DataFrame(rows)
        rxn_df.to_excel(
            f"{i}_ATP_related_fluxes_no_lactate.xlsx",
            index=False
        )