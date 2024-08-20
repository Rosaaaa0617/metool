import meta
from meta import results, utils, windows, plot2d
import os

from metaLiteral import CurveOpts

def main():
    models = utils.get_models('all')
    d3plot = models[0].name
    dir = os.path.dirname(d3plot)

    # path
    glstat = os.path.join(dir,"*")
    output = os.path.join(dir,"energy.jpg")
    
    # create window
    window_name = "energy"
    windows.Create2DPlotWindow(window_name)

    page_id = 0
    win = windows.Window(window_name,page_id)
    win.set_plots_settings({'legend':1})

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
        
    # set title off
    title = plot2d.Title(id=0, window_name=window_name, page_id=0)
    text = ""
    ret = title.set_text(text)
    
    # 3d sync nothing
    plot = plot2d.Plot(id=0, window_name=window_name, page_id=0)
    sync = "off"
    ret = plot.set_sync_select(sync)        
    
    # set axis title
    yaxis = plot2d.PlotAxis(id=0, type="yaxis", plot_id=0, window_name=window_name, page_id=0)
    title = "Energy"
    yaxis.set_title(title)
    xaxis = plot2d.PlotAxis(id=0, type="xaxis", plot_id=0, window_name=window_name, page_id=0)
    title = "Time"
    xaxis.set_title(title)
    
    # output window
    utils.MetaCommand(f'write jpeg "{output}" 85')
    
    
if __name__ == "__main__":
    os.system('cls')
    main()