import meta
from meta import results,utils,windows,plot2d
import os

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
    # glstat = os.path.join(dir,"binout*") # for mpp
    dir_all = os.path.join(dir,"*")
    
    # create window
    window_name = "Window1"
    windows.Create2DPlotWindow(window_name)

    # plot sliding
    plot_id = 1
    type = "glstat-Global"
    entities = ["1"]
    variables = ["Sliding interface energy (sie)"]
    sliding = plot2d.LoadCurvesDyna(
            window_name, plot_id, dir_all, type, entities, variables
        )
    # plot sliding
    plot_id = 2
    type = "sleout-Contact"
    entities = ["all"]
    variables = ["Total Friction Energy (tma)"]
    friction = plot2d.LoadCurvesDyna(
            window_name, plot_id, dir_all, type, entities, variables
        )    
    
def epnp():
    type = 'plain'
    name_type = 'Energy Needed to Prevent Penetration'
    x_formula = 'c1.x'
    y_formula = 'c1.y-c2.y'
    complex_formula = ''
    window = 'Window1'
    ret = plot2d.CurveFunctionUserDefined(type, name_type, x_formula, y_formula, complex_formula, window)
    print('c3.y')


    
if __name__ == "__main__":
    # now working for smp when result is loaded in meta
    main()
    epnp()