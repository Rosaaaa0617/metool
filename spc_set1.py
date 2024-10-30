import meta,time,os,platform
from typing import Tuple, List
from meta import results, utils, windows, plot2d, models, toolbars

from metaLiteral import *
import helpers


def xforce(dir):
    filename = os.path.join(dir,"binout*")
    
    # create window
    window_name = "bearing strength"
    windows.Create2DPlotWindow(window_name)
    
    page_id = 0
    win = windows.Window(window_name,page_id)
    
    all_curves = win.get_curves()
    all_curves: List[plot2d.Curve]
    if len(all_curves)>0:
        for cur in all_curves:
            cur.delete()
    
    # create curves
    utils.MetaCommand(f'xyplot read lsdyna "{window_name}" "{filename}" spcforc-Node 1 X_force_resultant_(xfr)')
    
    # set curve width
    all_curves = win.get_curves()
    for cur in all_curves:
        cur.set_line_width(2)
        cur.set_color(windows.Color(name="Red"))

        
    # set title off
    title = plot2d.Title(id=0, window_name=window_name, page_id=0)
    text = "bearing strength"
    ret = title.set_text(text)

    # 3d sync nothing
    plot = plot2d.Plot(id=0, window_name=window_name, page_id=0)
    sync = "off"
    ret = plot.set_sync_select(sync)        

    # set axis title
    helpers.axis_title(window_name,"Time","Force")
    
    # save xforce
    out = os.path.join(dir,"xforce.png")
    win.save_image(out)



def main():
    dir = helpers.get_current_model_dir()
    
    helpers.reload()
    views = ["top","left"]
    for view in views:
        helpers.save_gif_via_view(dir,view)
    
    xforce(dir)


# plot & save spc-force set1 and different views in gif
if __name__ == "__main__":
    helpers.NewScript()
    main()
