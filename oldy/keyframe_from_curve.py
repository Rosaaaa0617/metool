import meta, os
import numpy as np
from typing import List, Tuple
from meta import results, utils, spreadsheet, models, plot2d, windows

import metaLiteral


def reset():
    utils.MetaCommandList(
        ["window clearcreate 3d keepses",
         "report clear all",
         "spreadsheet clearall",
         "spreadsheet windows deleteall"]
        )
    
    
def load_animate(dir, states):
    window_name = 'MetaPost'
    filename = os.path.join(dir, "d3plot")
    deck = 'DYNA'
    r:models.Model = models.LoadModel(window_name, filename, deck, 'failed','on')
    
    model_id = r.id
    data = 'Stresses,VonMises,OuterSurface'
    scalar_resultsets = results.LoadScalar(model_id, filename, deck, states, data)
    
    data = 'Displacements'
    new_resultsets = results.LoadDeformations(model_id, filename, deck, states, data)
    
     
def load_curves(dir):
    filename = os.path.join(dir, "*")
    
    # create window
    window_name = "energy"
    windows.Create2DPlotWindow(window_name)

    # create curve
    plot_id = 0
    type = "glstat-Global"
    entities = ["1"]
    variables = metaLiteral.CurveOpts
    curves:List[plot2d.Curve] = plot2d.LoadCurvesDyna(window_name, plot_id, filename, type, entities, variables)
    
    for curve in curves:
        if curve.name == "Hourglass energy":
            return curve
        
    
def find_inflection_state(curve:plot2d.Curve, tEnd, dtplot):
    x:List[float] = curve.get_points_x_values()
    y:List[float] = curve.get_points_y_values('real')

    inflection_time = find_inflection_time(x, y)
    if not inflection_time:
        states = f"{tEnd/dtplot-10}-{tEnd/dtplot}"
    if inflection_time:
        states = f"{inflection_time/dtplot-5}-{inflection_time/dtplot+5}"
    
    return states
        
        
def find_inflection_time(x: List[float], y: List[float]):
    # 计算二阶导数
    dydx = [float(y[i + 1] - y[i]) / (x[i + 1] - x[i]) for i in range(len(x) - 1)]
    d2ydx2 = [dydx[i + 1] - dydx[i] for i in range(len(dydx) - 1)]
    
    # 找曲率最大的点
    curvature = [abs(d2ydx2[i]) / ((1 + dydx[i]**2)**(3/2)) for i in range(len(d2ydx2))]
    max_curvature_index = curvature.index(max(curvature))
    index = max_curvature_index + 1  
    
    t = (max(curvature) - curvature[index - 1]) / (curvature[index] - curvature[index - 1])
    inflection_time = x[index - 1] * (1 - t) + x[index] * t    
        
    return inflection_time
        
 
def output_gif(dir):
    win = windows.Window(name="MetaPost", page_id=0)

    # fringe active
    fringe_name = "default"
    fringe_type = "scalar"
    win.activate_fringe(fringe_name, fringe_type)

    # save as gif
    file = os.path.join(dir, "keyframe.gif")
    win.save_video(file, format="gif", loop_direction="forward")     


def main(dir, tEnd, d3plot):
    reset()
    curve = load_curves(dir)
    states = find_inflection_state(curve, tEnd, d3plot)
    load_animate(dir, states)
    output_gif(dir)
        
    
if __name__ == "__main__":
    dir = r"Z:\cae_jobs\geotech\pr-on-soil-inner\05-06_14-11"
    tEnd = 0.1
    dtplot = tEnd/200
    
    # dir = r"Z:\cae_jobs\truckhit\bus\vorbei\buscrush\pillow"
    # tEnd = 0.3
    # dtplot = tEnd/150
    
    main(dir, tEnd, dtplot)