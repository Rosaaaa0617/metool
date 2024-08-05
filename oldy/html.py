import meta
from meta import elements, constants, models, results, windows, utils, toolbars


# load scalar - strain energy
def load():
    m = models.Model(0)
    filename = m.name
    deck = 'DYNA'
    data_scalar = 'Displacements'
    
    all_types = results.DeformationTypes(filename, deck)
    one_type = all_types[0]
    total = len(one_type)

    step = max(total // 25, 1)  # 计算步长，确保总共有 25 个状态

    states = ",".join(str(i) for i in range(1, total, step))
        
    utils.MetaCommand('window active MetaPost')
    utils.MetaCommand(f'read geom Dyna3d "{filename}"')
         
    utils.MetaCommand(f'read dis Dyna3d "{filename}" "{states}" "{data_scalar}"')
    
def input():
    tb_name = 'my_toolbar'
    slider_name = 'step'
    textbox_name = 'save_name'
    output = toolbars.TextboxGetValue(tb_name,textbox_name)
    return output

def save(output):
    utils.MetaCommand('animation for')
    save_path = r"Z:/cae_jobs/naserve/metaml"
    utils.MetaCommand(f'write html3d {save_path}/{output}.html')

def main():
    output = input()
    load()
    save(output)
    
      
if __name__ == '__main__':
    main()