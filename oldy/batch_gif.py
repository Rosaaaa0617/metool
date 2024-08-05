import os
import meta
from meta import models, results, utils

def read_dyna_files(folder_path):
    d3plot_files = []  

    # 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 检查每个文件
        for file in files:
            if file == "d3plot":
                file_path = os.path.join(root, file)
                d3plot_files.append(file_path)  # 将.dyna文件内容添加到parts列表中
    
    # print(d3plot_files)
    return d3plot_files

def load_in_meta(d3plot):
    utils.MetaCommand('window clearcreate 3d keepses')
    utils.MetaCommand('report clear all')
    utils.MetaCommand('spreadsheet clearall')
    utils.MetaCommand('spreadsheet windows deleteall')
    
    window_name = "MetaPost"
    deck = "LSDYNA"
    r = models.LoadModel(window_name, d3plot, deck)
    
    model_id = 0
    states = "all"
    data = "Displacements"
    new_resultsets = results.LoadDeformations(model_id, d3plot, deck, states, data)

    utils.MetaCommand('animation for')
    save_path = os.path.dirname(os.path.dirname(d3plot))
    name = d3plot.split("\\")[-2]
    path = os.path.join(save_path,f"{name}.gif")
    utils.MetaCommand(f'record movie forward duration 3.76 gif "{path}"')



if __name__ == "__main__":
    
    total = r"Z:\cae_jobs\geotech"
    contents = os.listdir(total)
    subdirs = [f for f in contents if os.path.isdir(os.path.join(total, f))]
    print(subdirs)
    
    for subdir in subdirs:
        subdir_path = os.path.join(total,subdir)
        d3plot_files = read_dyna_files(subdir_path)        
        for d3plot in d3plot_files:
            if d3plot:
                print(d3plot)
                load_in_meta(d3plot)