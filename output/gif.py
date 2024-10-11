import re,os,meta
from meta import results, utils, windows, plot2d, models, toolbars
from enum import Enum
from typing import Tuple, List

import helpers
from metaLiteral import *


def main():
    dir = helpers.get_current_model_dir()
    
    name = "pre view"
    out = os.path.join(dir,name + '.gif')
    
    utils.MetaCommand('animation for')
    utils.MetaCommand(f'record movie forward duration 3.76 gif "{out}"')


if __name__ == "__main__":
    helpers.NewScript()
    main()
