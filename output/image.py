import re,os,meta
from meta import results, utils, windows, plot2d, models, toolbars
from enum import Enum
from typing import Tuple, List

import helpers
from metaLiteral import *

def get_next_image_number(directory):
    files = os.listdir(directory)
    image_files = [f for f in files if re.match(r'image\d+\.png', f)]
    
    if not image_files:
        return 'image1'
    
    max_num = 0
    for file in image_files:
        match = re.search(r'(\d+)', file)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    
    next_num = max_num + 1
    return f'image{next_num}'

def main():
    dir = helpers.get_current_model_dir()
    
    name = toolbars.TextboxGetValue('plot','name')
    if name == '':
        name = get_next_image_number(dir)
    
    out = os.path.join(dir,name + '.png')
    print(out)
    utils.MetaCommand(f'write png "{out}"')


if __name__ == "__main__":
    helpers.NewScript()
    main()
