import cobra
def fba(model, objective='curated_biomass'):
    model.objective=model.reactions.get_by_id(objective)
    model.objective_direction='max'
    result=model.optimize()
    return result
