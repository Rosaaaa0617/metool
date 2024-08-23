import meta
from meta import results,utils,windows,plot2d
import os,helpers

def plot_curves(dir):
    glstat = os.path.join(dir,"binout*")
    
    # create window
    window_name = "spcforce-z"
    windows.Create2DPlotWindow(window_name)

    # create curve
    plot_id = 1
    type = "spcforc-Node"
    entities = ['all']
    variables = ["Z force resultant (zfr)"]
    new_curves = plot2d.LoadCurvesDyna(window_name, plot_id, glstat, type, entities, variables)
    
    # set axis title
    helpers.axis_title(window_name,"Time(s)","F")
    
    return window_name
    

def spcforce_z():
    dir = helpers.get_current_model_dir()
    output = os.path.join(dir,"z-force.jpg")
    
    window_name = plot_curves(dir)
    
    # save plots
    helpers.save_win_plot(window_name,output)
    
if __name__ == "__main__":
    time = helpers.NewScript()
    #-------------------------
    spcforce_z()
    #-------------------------
    time.end()
    