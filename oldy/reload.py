import meta,os,helpers
from meta import results,utils,models,windows

def read_geo(d3plot:str):
    window_name = "MetaPost"
    deck = "DYNA"    
    models.LoadModel(window_name, d3plot, deck)

def read_deform(d3plot:str,states:str='all'):
    model_id = 0
    deck = "DYNA"
    data_scalar = 'Displacements'
    results.LoadDeformations(model_id, d3plot, deck, states, data_scalar)

def reload():
    dir = helpers.get_current_model_dir()
    d3plot = os.path.join(dir,'d3plot')
    
    read_deform(d3plot)
    
if __name__ == "__main__":
    time = helpers.NewScript()
    #-------------------------
    reload()
    #-------------------------
    time.end()
