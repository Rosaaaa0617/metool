import meta,time,os,platform
from typing import Tuple, List
from meta import results, utils, windows, plot2d, models, toolbars, guitk

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

    # set axis title
    helpers.axis_title(window_name,"Time","Force")
    

def save_video_via_view(dir:str,view:str):
    utils.MetaCommand(f'view default {view}')
    
    name = f"preview {view}"
    out = os.path.join(dir, name + '.avi')
    
    # win = windows.Window(name="MetaPost", page_id=0)
    # win.save_video(out, format="avi")
    
    utils.MetaCommand('record avi quality 100')
    utils.MetaCommand('record outputsize autoadjust enable')
    utils.MetaCommand(f'record movie forward loop 1 avi "{out}"')


def main():
    dir = helpers.get_current_model_dir()
    
    helpers.reload()
    xforce(dir)
    
    utils.MetaCommand('window autotile')
    utils.MetaCommand('window titlebars hide')
    
    win = windows.Window("MetaPost",0)
    win.activate()
    
    views = ["isometric"]
    for view in views:
        save_video_via_view(dir,view)
    
    


# plot & save spc-force set1 and different views in gif
if __name__ == "__main__":
    helpers.NewScript()
    main()
