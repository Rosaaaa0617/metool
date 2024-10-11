import meta,os,helpers
from meta import results,utils,models,windows

def reload():
    models = utils.get_models('all')
    d3plot = models[0].name
            
    utils.MetaCommand('window active MetaPost')
    utils.MetaCommand(f'read geom Dyna3d "{d3plot}"')
    utils.MetaCommand(f'read dis Dyna3d "{d3plot}" all Displacements')
    
if __name__ == "__main__":
    time = helpers.NewScript()
    #-------------------------
    reload()
    #-------------------------
    time.end()
