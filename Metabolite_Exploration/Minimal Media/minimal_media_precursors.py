import cobra
from set_DM_usage import set_dm
from run_fba_usage import fba

def id_essential_components(model, bm_precursor, media_condition): 
    tol=1e-6
    smodel, smedia=set_dm(model, media_condition)
    #these guilds represent individual units to remove to test, since some metabolites have compensating functions
    if media_condition == '52':
        media_guilds={'sulfur': ['EX_cys__L_e', 'EX_met__L_e'],
                      'cobalt': ['EX_cobalt2_e', 'EX_cbl1_e'],
                      'glu/arg': ['EX_glu__L_e', 'EX_arg__L_e'],
                      'aminobut':['EX_4abut_e'],
                    'ade':['EX_adn_e'],
                    'Ala':['EX_ala__L_e'],
                    'asn':['EX_asn__L_e'],
                    'asp':['EX_asp__L_e'],
                    'btn':['EX_btn_e'],
                    'ascb':['EX_ascb__L_e'],
                    'cit':['EX_cit_e'],
                    'csn':['EX_csn_e'],
                    'cu':['EX_cu2_e'],
                    'cytd':['EX_cytd_e'],
                    'fe':['EX_fe2_e'],
                    'fol':['EX_fol_e'],
                    'gluc':['EX_glc__D_e'],
                    'gly':['EX_gly_e'],
                    'gua':['EX_gua_e'],
                    'his':['EX_his__L_e'],
                    'ile':['EX_ile__L_e'],
                    'inos':['EX_inost_e'],
                    'k':['EX_k_e'],
                    'leu':['EX_leu__L_e'],
                    'lys':['EX_lys__L_e'],
                    'mg':['EX_mg2_e'],
                    'mn':['EX_mn2_e'],
                    'mop':['EX_mops_e'],
                    'na':['EX_na1_e'],
                    'nac':['EX_nac_e'],
                    'phe':['EX_phe__L_e'],
                    'pnto':['EX_pnto__R_e'],
                    'pro':['EX_pro__L_e'],
                    'pydx':['EX_pydx_e'],
                    'rib':['EX_ribflv_e'],
                    'ser':['EX_ser__L_e'],
                    'thm':['EX_thm_e'],
                    'thr':['EX_thr__L_e'],
                    'thym':['EX_thym_e'],
                    'trp':['EX_trp__L_e'],
                    'tyr':['EX_tyr__L_e'],
                    'ura':['EX_ura_e'],
                    'val':['EX_val__L_e'],
                    'xan':['EX_xan_e'],
                    'zn':['EX_zn2_e']}
    elif media_condition == '24':
        media_guilds={'glu/arg': ['EX_glu__L_e', 'EX_arg__L_e'],
                      'sulfur': ['EX_cys__L_e', 'EX_met__L_e'],
                      'asn':['EX_asn__L_e'],
                    'asp':['EX_asp__L_e'],
                    'ascb':['EX_ascb__L_e'],
                    'cit':['EX_cit_e'],
                    'cytd':['EX_cytd_e'],
                    'glc':['EX_glc__D_e'],
                    'his':['EX_his__L_e'],
                    'ile':['EX_ile__L_e'],
                    'k':['EX_k_e'],
                    'mg':['EX_mg2_e'],
                    'mops':['EX_mops_e'],
                    'nh4':['EX_nh4_e'],
                    'pro':['EX_pro__L_e'],
                    'ser':['EX_ser__L_e'],
                    'ura':['EX_ura_e'],
                    'val':['EX_val__L_e'],
                    'xan':['EX_xan_e']}
    elif media_condition == '16':
        media_guilds={'glu/arg': ['EX_glu__L_e', 'EX_arg__L_e'],
                      'asn':['EX_asn__L_e'],
                        'asp':['EX_asp__L_e'],
                        'cobalt':['EX_cobalt2_e'],
                        'cys':['EX_cys__L_e'],
                        'cytd':['EX_cytd_e'],
                        'glc':['EX_glc__D_e'],
                        'his':['EX_his__L_e'],
                        'ile':['EX_ile__L_e'],
                        'k':['EX_k_e'],
                        'mg':['EX_mg2_e'],
                        'mops':['EX_mops_e'],
                        'nh4':['EX_nh4_e'],
                        'pro':['EX_pro__L_e'],
                        'val':['EX_val__L_e']}
    elif media_condition == '13':
        media_guilds={'glu/arg': ['EX_glu__L_e', 'EX_arg__L_e'],
                  'asn':['EX_asn__L_e'],
                    'asp':['EX_asp__L_e'],
                    'cobalt':['EX_cobalt2_e'],
                    'cys':['EX_cys__L_e'],
                    'glc':['EX_glc__D_e'],
                    'his':['EX_his__L_e'],
                    'ile':['EX_ile__L_e'],
                    'k':['EX_k_e'],
                    'mg':['EX_mg2_e'],
                    'pro':['EX_pro__L_e'],
                    'val':['EX_val__L_e']}
    
    #Configure Model
    bm_precursor_dm = "DM_" + bm_precursor

    if bm_precursor_dm not in smodel.reactions:
        smodel.add_boundary(
            smodel.metabolites.get_by_id(bm_precursor),
            type='demand')

    smodel.objective = bm_precursor_dm

    #Run Simulation
    results=[]
    for guild_id, components in media_guilds.items(): 
        x=smodel.copy()
        for i in components:
            x.reactions.get_by_id(i).bounds=0,0
        y=fba(x, objective=bm_precursor_dm)
        if y.objective_value<tol:
            results.append(guild_id)
        else:
            continue 
    return results 

def id_supporting_components(model, bm_precursor, media_condition): 
    tol=1e-6
    #These are the components of the next most complex media that represent the search space for supporting components
    if media_condition== '24': 
        eligable_candidates={'EX_4abut_e': -0.238239650186896,
'EX_adn_e': -0.909023633807176,
'EX_ala__L_e': -3.43941818181818,
'EX_btn_e': -0.502788930606048,
'EX_csn_e': -0.44225513460437,
'EX_cu2_e': -0.000983950365558824,
'EX_fe2_e': -0.0323445102064021,
'EX_fol_e': -0.000556576183218685,
'EX_gly_e': -0.837744,
'EX_gua_e': -0.487671661363185,
'EX_inost_e': -0.00681833698681884,
'EX_leu__L_e': -0.468006545454545,
'EX_lys__L_e': -0.881965090909091,
'EX_mn2_e': -0.0221638272953635,
'EX_na1_e': -0.0840769087175658,
'EX_nac_e': -0.0402313481163887,
'EX_phe__L_e': -0.371702836363636,
'EX_pnto__R_e': -0.00515545143585351,
'EX_pydx_e': -0.0120652552437249,
'EX_ribflv_e': -0.0130548864158699,
'EX_thm_e': -0.185161838463014,
'EX_thr__L_e': -0.515417920291105,
'EX_thym_e': -0.0584424852762019,
'EX_trp__L_e': -0.336817309090909,
'EX_tyr__L_e': -0.271098358335077,
'EX_zn2_e': -0.00854216715134657}
        
    elif media_condition== '16':
        eligable_candidates={'EX_ascb__L_e': -0.697458344517168,'EX_cit_e': -2.17226868802977,'EX_met__L_e': -0.164648969420768,'EX_ser__L_e': -1.81153897697883,'EX_ura_e': -0.00438361724922243,'EX_xan_e': -0.0193811894502184}
        
    elif media_condition=='13':
        eligable_candidates={'EX_cytd_e': -0.101009685701545,'EX_mops_e': -9.82706405984726,'EX_nh4_e': -7.08581509092581,}

    #Configure model
    smodel, smedia=set_dm(model, media_condition)

    bm_precursor_dm = "DM_" + bm_precursor

    if bm_precursor_dm not in smodel.reactions:
        smodel.add_boundary(
            smodel.metabolites.get_by_id(bm_precursor),
            type='demand'
        )

    smodel.objective = bm_precursor_dm

    #Run Simulation
    results=[]
    wt_flux=fba(smodel, objective=bm_precursor_dm)
    for component, concentration in eligable_candidates.items():
        x=smodel.copy()
        x.reactions.get_by_id(component).lower_bound=concentration
        y=fba(x, objective=bm_precursor_dm)
        if y.objective_value>(wt_flux.objective_value+tol):
            results.append(component)
    
    return results

def generate_Figure(results, filename, title=None, label_map=None):
    """
    results: dict
        {precursor_id: [component1, component2, ...]}

    filename: str
        Output file path, e.g. "essential_components.svg"

    label_map: dict, optional
        Pretty labels for precursor IDs or component IDs.
    """

    import matplotlib.pyplot as plt
    import pandas as pd

    if label_map is None:
        label_map = {}

    # Convert results dictionary to long format
    rows = []
    for precursor, components in results.items():
        for component in components:
            rows.append({
                "precursor": precursor,
                "component": component,
                "required": 1
            })

    if len(rows) == 0:
        print(f"No results to plot for {filename}")
        return

    df = pd.DataFrame(rows)

    # Count requirements per precursor and per component
    precursor_order = (
        df.groupby("precursor")["component"]
        .nunique()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    component_order = (
        df.groupby("component")["precursor"]
        .nunique()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    # Put the most common component at the top
    component_order = component_order[::-1]

    # Make binary matrix so missing combinations can be shown as open dots
    matrix = pd.DataFrame(
        0,
        index=component_order,
        columns=precursor_order
    )

    for _, row in df.iterrows():
        matrix.loc[row["component"], row["precursor"]] = 1

    fig_width = max(7, 0.75 * len(precursor_order))
    fig_height = max(4, 0.55 * len(component_order))

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Plot all possible combinations as open gray circles
    for y, component in enumerate(component_order):
        for x, precursor in enumerate(precursor_order):
            if matrix.loc[component, precursor] == 1:
                ax.scatter(
                    x, y,
                    s=70,
                    facecolors="black",
                    edgecolors="black",
                    linewidths=1.2
                )
            else:
                ax.scatter(
                    x, y,
                    s=45,
                    facecolors="white",
                    edgecolors="0.75",
                    linewidths=1.2
                )

    ax.set_xticks(range(len(precursor_order)))
    ax.set_yticks(range(len(component_order)))

    ax.set_xticklabels(
        [label_map.get(x, x) for x in precursor_order],
        rotation=50,
        ha="right",
        fontsize=11
    )

    ax.set_yticklabels(
        [label_map.get(y, y) for y in component_order],
        fontsize=11
    )

    ax.set_xlim(-0.5, len(precursor_order) - 0.5)
    ax.set_ylim(-0.5, len(component_order) - 0.5)

    ax.tick_params(axis="both", length=0)

    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
        spine.set_color("black")

    if title is not None:
        ax.set_title(title, fontsize=14)

    ax.set_xlabel("")
    ax.set_ylabel("")

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()

def run_simulation(model, essential_med, support_med, base_filename):
    bm_precusor_list = [
        'M8801_c', 'M8807_c', 'M8811_c',
        'e_Cofactor_c', 'e_DNA_c', 'e_Lipid_c',
        'e_Protein_c', 'e_RNA_c'
    ]

    essential_component_results = {}
    supporting_component_results = {}

    for i in bm_precusor_list:
        essential_component_results[i] = id_essential_components(model, i, essential_med)

        if essential_med != support_med:
            supporting_component_results[i] = id_supporting_components(model, i, support_med)

    essential_filename = base_filename + "_" + essential_med + "_essential_components.svg"
    generate_Figure(essential_component_results, essential_filename)

    if essential_med != support_med:
        supporting_filename = base_filename + "_" + support_med + "_supporting_components.svg"
        generate_Figure(supporting_component_results, supporting_filename)

########
model=cobra.io.read_sbml_model('iGR385.xml')

base_filename=str('Sim')

run_simulation(model, '52', '24', base_filename)
run_simulation(model, '24', '16', base_filename)
run_simulation(model, '16', '13', base_filename)
run_simulation(model, '13', '13', base_filename)