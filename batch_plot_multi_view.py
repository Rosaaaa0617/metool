import shutil,os,meta
from meta import results, utils, windows, plot2d, models, toolbars
from enum import Enum

def new_script():
    utils.MetaCommand('window clearcreate 3d keepses')
    utils.MetaCommand('report clear all')
    utils.MetaCommand('spreadsheet clearall')
    utils.MetaCommand('spreadsheet windows deleteall')


class CurveOpts(str,Enum):
    KE = "Kinetic energy (ke)"
    IE = "Internal energy (ie)"
    HE = "Hourglass energy (he)"
    # sliding
    SIE = "Sliding interface energy (sie)"
    TE = "Total energy (te)"


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
    yaxis = plot2d.PlotAxis(id=0, type="yaxis", plot_id=0, window_name=window_name, page_id=0)
    title = "Energy"
    yaxis.set_title(title)
    xaxis = plot2d.PlotAxis(id=0, type="xaxis", plot_id=0, window_name=window_name, page_id=0)
    title = "Time"
    xaxis.set_title(title)
    
    # output window
    utils.MetaCommand(f'write jpeg "{output}" 85')
    
    
def get_partition_states(filename,deck,n):
    all_types = results.DeformationTypes(filename, deck)
    print('----------',len(all_types))
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
            
    # get the total states
    indices = get_partition_states(d3plot,deck,n)
    print(indices)
    
    # plot results
    model_id = 0
    states = indices
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


def copy_paste(source_folder, target_folder):
    # copy file
    extensions = ('.jpg', '.png')
    for image_file in os.listdir(source_folder):
        if image_file.lower().endswith(extensions):
            source_file = os.path.join(source_folder, image_file)
            paste_file = os.path.join(target_folder, image_file)
            
            shutil.copy2(source_file, paste_file)
            
    print(f'Copied to {target_folder}')


def subdirs_in_path(path:str):
    contents = os.listdir(path) # all files + directors in total
    subdirs = [f for f in contents if os.path.isdir(os.path.join(path, f))] # pick directors in total
    return subdirs


def meta_prozess(folder, n):
    d3plot = os.path.join(folder,'d3plot')
    # meta prozess
    new_script()
    loaded_results(d3plot, n)
    views = ['top', 'front', 'right','left']
    # views = ['left']
    for view in views:
        save_metapost(folder,view)
    plot_energy(folder)

# delete image files in directory
def delete_image_files(directory, extensions=(".jpg", ".png")):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"delete: {file_path}")

def single(car_dir,name,n,stamped):
    folder = os.path.join(r'z:/cae_jobs',car_dir,name)
    delete_image_files(folder)
    meta_prozess(folder,n)
    
    dir_in_stamped = os.path.join(stamped,car_dir,name)
    remove_dir(dir_in_stamped)
    copy_paste(folder, dir_in_stamped)
    
    
def remove_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)
        print(f'exist {dir} and delete')
        os.mkdir(dir)    

def count_visible_directory_contents(dir_path):
    visible_contents = [f for f in os.listdir(dir_path) if not f[0] == '.']
    return len(visible_contents)     
        
# used for simulation before sb
def batch_1(car_dir):
    dir = os.path.join(r'z:/cae_jobs',car_dir)
    subdirs = subdirs_in_path(dir)
    
    subdirs_path = [item for item in subdirs if item.startswith('08')]
    for name in subdirs_path:
        folder = os.path.join(dir,name)
        print(folder)
        num = count_visible_directory_contents(folder)
        if num > 1:
            # delete_image_files(folder)
            meta_prozess(folder,n)
            
            stamped = os.path.join(r'd:/Users/ADMIN/Desktop/results',car_dir,name)
            print(stamped)
            remove_dir(stamped)
            copy_paste(folder,stamped)
            
    

if __name__ == "__main__":
    os.system('cls') 
    #-----------------------------
    n = 3

    # car_dir = 'smallcar'
    car_dir = 'bus'
    # car_dir = 'truck'
    
    name = r'07-09_17-34_succeed'
    stamped = r'd:/Users/ADMIN/Desktop/results'
    #-----------------------------
    car_dirs = ['smallcar', 'bus', 'truck']
    for car_dir in car_dirs:
        batch_1(car_dir)
    #-----------------------------
    # single(car_dir, name, n, stamped)
    #-----------------------------
    # # batch
    # dir = r'z:/cae_jobs/sb'
    
    # subdirs = subdirs_in_path(dir)
    # # print(subdirs)
    
    # for subdir in subdirs:
    #     subdir_path = os.path.join(dir,subdir)
    #     cars = subdirs_in_path(subdir_path)
    #     # print(cars)
    #     for car in cars:
    #         folder = os.path.join(dir,subdir,car)
    #         print(folder)
    #         num = count_visible_directory_contents(folder)
    #         if num > 1:
    #             print(f'{num} files in {folder}')
    #             # delete_image_files(folder)
    #             meta_prozess(folder,n)
            
            
    #             dir_in_stamped = os.path.join(stamped,car,subdir)
    #             print(dir_in_stamped)
    #             remove_dir(dir_in_stamped)
    #             copy_paste(folder,dir_in_stamped)

    
    print('--------------all done---------------------')
    
    
