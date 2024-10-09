import meta,time,os,platform
from meta import results, utils, windows, plot2d, models, toolbars

from metaLiteral import *

class NewScript():
    def __init__(self):
        if platform.system() == "Windows":
            os.system('cls')  # Windows命令清屏
        else:
            os.system('clear') 

        print('hakuna matata','\n\n')
        self.start_time = time.time()
    
    def end(self):
        end_time = time.time()
        elapse_time = end_time - self.start_time
        print(f"ELAPSE TIME:{elapse_time} S\n")


def clear_all():
    utils.MetaCommand('window clearcreate 3d keepses')
    utils.MetaCommand('report clear all')
    utils.MetaCommand('spreadsheet clearall')
    utils.MetaCommand('spreadsheet windows deleteall')
    
    print('drop your file')
        

def axis_title(win_name:str,xaxis_title:str,yaxis_title:str):
    yaxis = plot2d.PlotAxis(id=0, type="yaxis", plot_id=0, window_name=win_name, page_id=0)
    yaxis.set_title(yaxis_title)
    xaxis = plot2d.PlotAxis(id=0, type="xaxis", plot_id=0, window_name=win_name, page_id=0)
    xaxis.set_title(xaxis_title)

def get_current_model_dir():
    models = utils.get_models('all')
    d3plot = models[0].name
        
    return os.path.dirname(d3plot)

def save_win_plot(win_name:str,filename:str):
    win = windows.Window(name=win_name,page_id=0)
    win.save_image(filename)
    print("Saving file", filename)


def subdirs_in_path(path:str):
    '''
    return List[director name]
    '''
    contents = os.listdir(path) # all files + directors in total
    subdirs = [f for f in contents if os.path.isdir(os.path.join(path, f))] # pick directors in total
    return subdirs


if __name__ == "__main__":
    NewScript()
    nog = "thx to ansa's vfs, need run this script before run anything in examples"
    print(nog)
