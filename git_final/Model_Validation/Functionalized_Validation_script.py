#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:58:02 2026

@author: grichmond
"""
import cobra
from set_DM_usage import set_dm 
from run_fba_usage import fba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calc_CM(model, media_str, IV_data, title, fig_file):
    """
    Parameters
    ----------
    model : CB model
        cobra model file.
    media_str : str
        Media condition to run validation against.
    IV_data : file
        Excel file of the IV data from experiments.
    title: str
        Title of the CM 
    fig_file : str
        name of the resulting CM figure.

    Returns
    -------
    metrics_dict : dict
        model performance metrics coming from the confusion matrices.

    """
    tmodelc, media_dict = set_dm(model, media_str)
    x = fba(tmodelc)

    result = {}
    is_fc = {}

    for rxn, concentration in media_dict.items():
        tmodelc2 = tmodelc.copy()

        rxn2 = tmodelc2.reactions.get_by_id(rxn.id)
        rxn2.lower_bound = 0

        y = fba(tmodelc2)

        result[rxn.id] = y.objective_value
        is_fc[rxn.id] = y.objective_value / x.objective_value

    is_fc = pd.DataFrame.from_dict(is_fc, orient='index', columns=['IS'])
    is_fc.index.name = 'exchange'

    iv_data = pd.read_excel(IV_data, na_values=["#N/A"])

    media_col = int(media_str) if media_str.isdigit() else media_str

    iv_data = iv_data[['exchange', media_col]].rename(columns={media_col: 'IV'})
    iv_data.set_index('exchange', inplace=True)

    merged_fcs = iv_data.join(is_fc, how='inner').reset_index()
    if media_str=='52':
        excluded=['EX_inost_e','EX_ala__L_e','EX_lys__L_e','EX_gua_e','EX_thr__L_e','EX_pnto__R_e','EX_csn_e','EX_cu2_e','EX_pydx_e','EX_leu__L_e','EX_ribflv_e','EX_na1_e','EX_thm_e','EX_mn2_e','EX_thym_e','EX_phe__L_e','EX_fe2_e','EX_zn2_e','EX_fol_e','EX_nac_e','EX_cbl1_e','EX_btn_e','EX_gly_e','EX_trp__L_e','EX_tyr__L_e','EX_4abut_e','EX_adn_e']
    elif media_str=='24':
        excluded=['EX_cit_e','EX_ura_e','EX_xan_e','EX_met__L_e']
    elif media_str=='16':
        excluded=['EX_cytd_e','EX_mops_e','EX_nh4_e']
    elif media_str=='13':
        excluded=[]
    elif media_str=='Sun_et_al':
        excluded=[]
    TP = 0
    FN = 0
    TN = 0
    FP = 0
    matrix = {}
    tp_list = []
    fn_list = []
    tn_list = []
    fp_list = []

    for _, results in merged_fcs.iterrows():
        exchange = results['exchange']
        
        IV_label = "no_effect" if results['IV'] > 0.8 else "deleterious"
        IS_label = "no_effect" if results['IS'] > 0.8 else "deleterious"
        
        matrix[exchange] = (IV_label, IS_label)
        
        if IV_label == "deleterious" and IS_label == "deleterious":
            TP += 1
            tp_list.append(exchange)
            
        elif IV_label == "deleterious" and IS_label == "no_effect":
            if exchange in excluded:
                TN += 1
                tn_list.append(exchange)
            else:
                FN += 1
                fn_list.append(exchange)
                
        elif IV_label == "no_effect" and IS_label == "no_effect":
            TN += 1
            tn_list.append(exchange)
            
        elif IV_label == "no_effect" and IS_label == "deleterious":
            FP += 1
            fp_list.append(exchange)


    total = TP + TN + FP + FN
    accuracy = (TP + TN) / total if total > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0  # same as TPR
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0
    fpr = FP / (FP + TN) if (FP + TN) > 0 else 0

    cm = np.array([[TN, FP],
                   [FN, TP]])

    metrics_text = (f"Accuracy={accuracy:.3f} | Recall={recall:.3f} | Precision={precision:.3f} | "
                    f"Specificity={specificity:.3f} | FPR={fpr:.3f} ")
    
    metrics_dict={"Accuracy": accuracy,
                  "Recall": recall, 
                  "Precision": precision,
                  "Specificity": specificity,
                  "FPR": fpr}

    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Predicted No Effect', 'Predicted Deleterious'])
    ax.set_yticklabels(['Actual No Effect', 'Actual Deleterious'])
    title = str(title + "\n")
    ax.set_title(title + metrics_text, fontsize=14, fontweight='bold', pad=20)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            ax.text(j, i, cm[i, j], ha="center", va="center", color=color, fontsize=20)

    plt.tight_layout()
    plt.savefig(fig_file, format="svg") 
    plt.show()
    
    return metrics_dict, cm

#####RUNNING######
model=cobra.io.read_sbml_model("iGR385.xml")

media_test_list=['52', '24', '16', '13', 'Sun_et_al']
media_colors = ['#6f9969', '#5c66a8', '#808fe1', '#454a74']
cms={}
concat_data_dict={}
for media in media_test_list:
    descriptive_DM= str("DM"+media)
    x,y=calc_CM(model, media, 'iv_fc_EX.xlsx', descriptive_DM, str("CM_"+descriptive_DM+".svg"))
    concat_data_dict[media]=x
    cms[media]=y        #cm = np.array([[TN, FP][FN, TP]])    