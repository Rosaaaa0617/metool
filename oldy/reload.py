import meta
from meta import results
from meta import utils
import os

def main():
    models = utils.get_models('all')
    path = None

    for model in models:
        if model.id == 0:
            path = model.name
            break  # 停止循环，因为已经找到 ID 为 0 的模型

    if path is not None:
        directory = os.path.dirname(path)
            
    utils.MetaCommand('window active MetaPost')
    utils.MetaCommand(f'read geom Dyna3d "{path}"')
    utils.MetaCommand(f'read dis Dyna3d "{path}" all Displacements')
    
if __name__ == "__main__":
    main()