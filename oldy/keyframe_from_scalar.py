import meta, os
from meta import results, utils, spreadsheet, models, plot2d, windows


def reset():
    utils.MetaCommandList(
        ["window clearcreate 3d keepses",
         "report clear all",
         "spreadsheet clearall",
         "spreadsheet windows deleteall"]
        )
    
def find_key_state(new_resultsets):
    m = models.Model(0)
    
    for res in new_resultsets:
        scalar = m.get_nodal_scalar(res, specifier='max', numpy='value')
        max_scalar = scalar[0]
        
        if max_scalar >= 10*0.98:
            return res.state
        
    return None

def load(states, d3plot_path):
    window_name = 'MetaPost'
    filename = d3plot_path
    deck = 'DYNA'
    r = models.LoadModel(window_name, filename, deck, 'failed','on')

    model_id = r.id
    data = 'Stresses,VonMises,OuterSurface'
    scalar_resultsets = results.LoadScalar(model_id, filename, deck, states, data)
    
    data = 'Displacements'
    new_resultsets = results.LoadDeformations(model_id, filename, deck, states, data)
    
    return scalar_resultsets
 
def main(d3plot_path):
    reset()
    states = 'all'
    scalar_resultsets = load(states, d3plot_path)
    key_state = find_key_state(scalar_resultsets)
    
    reset()
    states = f'{key_state-5}-{key_state+5}'
    load(states, d3plot_path)
    
        
    # win = windows.Window(name="MetaPost", page_id=0)
    # fringe_name = "OIC_Simulation_palette"
    # fringe_type = "scalar"
    # win.activate_fringe(fringe_name, fringe_type)
    
if __name__ == "__main__":
    d3plot_path = r"Z:\cae_jobs\geotech\pr-on-soil-inner\05-06_14-11\d3plot"
    main(d3plot_path)