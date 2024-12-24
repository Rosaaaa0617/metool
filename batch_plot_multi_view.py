import shutil,os,meta
from meta import results, utils, windows, plot2d, models, toolbars
from enum import Enum
from typing import Tuple, List

import helpers
from metaLiteral import *


def plot_energy(source_folder):
    # create window
    window_name = "energy"
    windows.Create2DPlotWindow(window_name)
    
    page_id = 0
    win = windows.Window(window_name,page_id)
    win.set_plots_settings({'legend':1})

    # path
    glstat = os.path.join(source_folder,"*")
    output = os.path.join(source_folder,"energy.jpg")

    # create curve
    plot_id = 1
    type = "glstat-Global"
    entities = ["1"]
    variables = CurveOpts # enum is default a iterater, filter out some you don't want to plot
    
    new_curves = plot2d.LoadCurvesDyna(window_name, plot_id, glstat, type, entities, variables)
    
    # set curve width
    all_curves = win.get_curves()
    for cur in all_curves:
        cur.set_line_width(2)
    
    # set axis title
    helpers.axis_title(window_name,"Time","Energy")
    
    # output window
    utils.MetaCommand(f'write jpeg "{output}" 100')
    
    
def get_partition_states(filename,deck,n):
    all_types = results.DeformationTypes(filename, deck)
    print('----------',len(all_types),'states')
    if len(all_types) == 0 :
        indices = [0]
    else:
        displa = all_types[0]
        base_size, remainder = divmod(len(displa), n)
        indices = [(i + 1) * base_size + min(i, remainder) - 1 for i in range(n)]
        indices.insert(0,0)  # state 0
    return indices

    
def loaded_results(d3plot,n):
    window_name = "MetaPost"
    deck = "LSDYNA"
    r = models.LoadModel(window_name, d3plot, deck)
            
    if n == 0:
        states = '0'
    else:
        # get the total states
        indices = get_partition_states(d3plot,deck,n)
        print(indices)
        states = indices
        
    # plot results
    model_id = 0
    data_scalar = 'Displacements'
    results.LoadDeformations(model_id, d3plot, deck, str(states), data_scalar)


def save_metapost(source_folder,view:str):
    win = windows.Window(name="MetaPost", page_id=0)
    m = models.Model(0)
    all_res = m.get_resultsets()
    
    utils.MetaCommand(f'view default {view}')
    
    for i in range(0,len(all_res)):
        print(i)
        win.set_current_resultset(m, all_res[i])
        file = os.path.join(source_folder,f'{view} state{i}.png')
        win.save_image(file)
    print('states have been saved')


def save_metapost_bestview(source_folder):
    win = windows.Window(name="MetaPost", page_id=0)
    m = models.Model(0)
    all_res = m.get_resultsets()
    win.set_current_resultset(m, all_res[0])
    
    utils.MetaCommand(f'view set -2918.98,-1552.13,527.816,-755.179,-3763.01,-565.617,0.314816,-0.155008,0.93641,-755.179,-3763.01,-565.617,-168874,175437,28,0')
    file = os.path.join(source_folder,f'best view 1.png')
    win.save_image(file)
    
    utils.MetaCommand(f'view set -4045.55,-2001.25,423.33,1954.29,3998.52,-4474.84,0.35352,0.353517,0.866054,1954.29,3998.52,-4474.84,-104973,124568,28,0')
    file = os.path.join(source_folder,f'best view 2.png')
    win.save_image(file)
    print('states have been saved')


def copy_paste(source_folder, target_folder):
    remove_recreate_dir(target_folder)
    # copy file
    extensions = ('.jpg', '.png')
    for image_file in os.listdir(source_folder):
        if image_file.lower().endswith(extensions):
            source_file = os.path.join(source_folder, image_file)
            paste_file = os.path.join(target_folder, image_file)
            
            shutil.copy2(source_file, paste_file)
            
    print(f'Copied to {target_folder}')


# delete image files in directory
def delete_image_files(directory, extensions=(".jpg", ".png")):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"delete: {file_path}")

    
# folder must be full path
def single(folder, n, views:List[str]=None, redo:bool=True):
    if redo:
        delete_image_files(folder)
        
    d3plot = os.path.join(folder,'d3plot')
    if os.path.exists(d3plot):
        helpers.clear_all()
        loaded_results(d3plot, n)
        save_metapost_bestview(folder) 
        if views:
            for view in views:
                save_metapost(folder,view)  # plot multi views
        # plot_energy(folder)
    else:
        print(f'{d3plot} not exist')
                
                
def remove_recreate_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        print(f'delete {dir} and recreate')
    os.makedirs(dir)    
        
        
# used for simulation before sb
def batch_1(car_dir, n, views:List[str]=None, redo:bool=True):
    base_dir = os.path.join(r'E:\#chen\metool\test\befor',car_dir)
    time_dirs = helpers.subdirs_in_path(base_dir)
    
    subdirs_path = [item for item in time_dirs if item.startswith('08')]
    for time in subdirs_path:
        folder = os.path.join(base_dir,time)
        print(folder)

        single(folder, n, views, redo)
            
        stamped = os.path.join(r'E:\#chen\metool\test\res',car_dir,time)
        print(stamped)
        copy_paste(folder,stamped)
            
            
# used for simulation in sb
def batch_sb(res_path,n,views:List[str]=None,redo:bool=True):
    base_dir = r'E:\#chen\metool\test\simu'
    time_dirs = helpers.subdirs_in_path(base_dir)
    print("turn to---------",time_dirs)
    
    for time_dir in time_dirs:
        time_fullpath = os.path.join(base_dir,time_dir)
        cars = helpers.subdirs_in_path(time_fullpath)
        print("car---------",cars)
        for car in cars:
            folder = os.path.join(base_dir,time_dir,car)
            
            single(folder, n, views, redo)
            
            dir_in_stamped = os.path.join(res_path,car,time_dir)
            print(dir_in_stamped)
            copy_paste(folder,dir_in_stamped)


if __name__ == "__main__":
    time = helpers.NewScript()
    #-----------------------------
    n = 2

    # car_dir = 'smallcar'
    car_dir = 'bus'
    # car_dir = 'truck'
        
    # views = ['top', 'right', 'isometric']
    views = ['left']
    
    res = r'E:\#chen\metool\test\res'
    #-----------------------------
    # batch_1(car_dir,n,views)
    batch_sb(res,n,views,True)

    
    print('-----------all done------------')
    #-----------------------------
    time.end
    
