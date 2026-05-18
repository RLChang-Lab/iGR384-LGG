#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:33:19 2026

@author: grichmond
"""

from set_DM_usage import set_dm 
from PE_utils_usage_single import pe_Data, plot_production_envelope_single
from cobra.io import read_sbml_model 

model= read_sbml_model('iGR385.xml')
media={'52': '#6e9869', '24': '#5c67a8'}

for media_name, color in media.items():
    model_run= model.copy()
    model_set, media_dict= set_dm(model_run, media_name) #set media conditon 
    results_lac=pe_Data(model_set, target='EX_lac__L_e', num_points=10) #generate production env data for lactate in media condition
    results_i3a=pe_Data(model_set, target='EX_i3a_e', num_points=10) #generate a production env data for i3a in media condition
    title_lac= str( media_name + " Lactate Flux PE")
    filename_lac= str( media_name + "_lac_PE")
    title_i3a= str( media_name + " I3A Flux PE")
    filename_i3a= str( media_name + "_i3a_PE")
    plot_production_envelope_single(results_lac, media_name,"Directory",title_lac, filename=filename_lac, xlab="biomass flux", ylab='lactate secretion flux', color_pick=color)
    plot_production_envelope_single(results_i3a, media_name, "Directory" ,title_i3a, filename=filename_i3a, xlab="biomass flux", ylab='I3A secretion flux', color_pick=color)
    
    