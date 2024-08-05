import meta
from meta import results,utils,windows,plot2d

def main():
    utils.MetaCommand('opt ses controldraw push')
    utils.MetaCommand('opt ses controldraw dis')
    utils.MetaCommand('0:era pid 4-73')
    utils.MetaCommand('opt ses controldraw pop')


if __name__ == "__main__":
    main()