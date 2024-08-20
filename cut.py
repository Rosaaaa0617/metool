import meta
from meta import results,utils,windows,plot2d,toolbars,models
import os

from metaLiteral import CurveOpts

def get_current_model_dir():
    models = utils.get_models('all')
    d3plot = models[0].name
        
    return os.path.dirname(d3plot)
        
        
def get_partition_indices(filename,deck,n):
    all_types = results.DeformationTypes(filename, deck)
    displa = all_types[0]
    base_size, remainder = divmod(len(displa), n)
    indices = [(i + 1) * base_size + min(i, remainder) - 1 for i in range(n)]
    return indices


def clear():
    # delete states
    m = models.Model(0)
    res = m.get_current_resultset()
    res.delete()
    
    
def loaded_results():
    m = models.Model(0)
    filename = m.name
    deck = 'DYNA'
    data_scalar = 'Displacements'
        
    # get the total states
    n = get_toolbar_value()
    # n = 5
    indices = get_partition_indices(filename,deck,n+1)
    print(indices)
    
    # plot results
    model_id = 0
    states = indices
    results.LoadDeformations(model_id, filename, deck, str(states), data_scalar)

    
def get_toolbar_value():
    n = toolbars.SliderGetValue('report','num')
    return n


def save_plot():
    dir = get_current_model_dir()
    win = windows.Window(name="MetaPost", page_id=0)
    m = models.Model(0)
    all_res = m.get_resultsets()
    for i in range(0,len(all_res)):
        print(i)
        win.set_current_resultset(m, all_res[i+1])
        file = os.path.join(dir,f'state{i+1}.png')
        win.save_image(file)


if __name__ == "__main__":
    os.system('cls')
    # dir = get_current_model_dir()
    # loaded_results()
    # save_plot(dir)
    clear()
