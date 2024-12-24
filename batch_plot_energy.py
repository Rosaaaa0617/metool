import meta
from meta import results, utils, windows, plot2d, models, toolbars
import os,helpers

from metaLiteral import CurveOpts

def find_dyna_files(folder_path):
    d3plot_files = []  

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "d3plot":
                file_path = os.path.join(root, file)
                d3plot_files.append(file_path)  

    return d3plot_files

def dirs_in_path(path:str):
    contents = os.listdir(path) # all files + directors in total
    subdirs = [f for f in contents if os.path.isdir(os.path.join(path, f))] # pick directors in total
    return subdirs


def plot_energy(d3plot):
    # create window
    window_name = "energy"
    windows.Create2DPlotWindow(window_name)
    
    page_id = 0
    win = windows.Window(window_name,page_id)
    win.set_plots_settings({'legend':1})

    # path
    dir = os.path.dirname(d3plot)
    glstat = os.path.join(dir,"*")
    output = os.path.join(dir,"energy.jpg")

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
    utils.MetaCommand(f'write jpeg "{output}" 85')

def main():
    os.system('cls')
    
    path = toolbars.TextboxGetValue('report', 'root')
    subdirs = dirs_in_path(path)
    
    d3plot = []
    for subdir in subdirs:
        if subdir.startswith(toolbars.TextboxGetValue('report', 'filter')):
            subdir_path = os.path.join(path,subdir)
            d3plot.extend(find_dyna_files(subdir_path))
    
    for d in d3plot:
        helpers.new_script()
        plot_energy(d)

               
    
    
if __name__ == "__main__":
    os.system('cls')
    
    path = r"Z:\cae_jobs\bus"
    subdirs = dirs_in_path(path)
    
    d3plot = []
    for subdir in subdirs:
        if subdir.startswith("08"):
            subdir_path = os.path.join(path,subdir)
            d3plot.extend(find_dyna_files(subdir_path))
            
    helpers.new_script()
    plot_energy(d3plot[0])
                
