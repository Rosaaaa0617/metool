import meta
from meta import results, utils, windows, plot2d
import os

from metaLiteral import CurveOpts

def main():
    models = utils.get_models('all')
    path = None

    for model in models:
        if model.id == 0:
            path = model.name
            break  # 停止循环，因为已经找到 ID 为 0 的模型

    if path is not None:
        dir = os.path.dirname(path)

    # path
    glstat = os.path.join(dir,"*")
    output = os.path.join(dir,"energy.jpg")
    
    # create window
    window_name = "energy"
    windows.Create2DPlotWindow(window_name)

    # create curve
    plot_id = 1
    type = "glstat-Global"
    entities = ["1"]
    variables = CurveOpts # enum is default a iterater, filter out some you don't want to plot
    
    new_curves = plot2d.LoadCurvesDyna(
            window_name, plot_id, glstat, type, entities, variables
        )
    
    # set axis title
    yaxis = plot2d.PlotAxis(
        id=0, type="yaxis", plot_id=0, window_name=window_name, page_id=0
    )
    title = "energy"
    yaxis.set_title(title)
    
    xaxis = plot2d.PlotAxis(
        id=0, type="xaxis", plot_id=0, window_name=window_name, page_id=0
    )
    title = "time"
    xaxis.set_title(title)
    
    
    # output window
    utils.MetaCommand(f'write jpeg "{output}" 85')
    
    
if __name__ == "__main__":
    main()