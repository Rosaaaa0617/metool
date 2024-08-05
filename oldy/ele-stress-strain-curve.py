import meta
from meta import utils


models = utils.get_models('all')
path = None
for model in models:
    if model.id == 0:
        path = model.name
        break  # 停止循环，因为已经找到 ID 为 0 的模型

if path is not None:
    print(f"ID为0的模型的名称是：{path}")

    utils.MetaCommand(f"opt var elempick p1")

    utils.MetaCommand(f"read dis Dyna3d {path} All Displacements")
    utils.MetaCommand(f"read onlyfun Dyna3d {path} All Strains,FullTensor(UCS),Outer Surface")
    utils.MetaCommand("function append scalar enable")
    utils.MetaCommand(f"read onlyfun Dyna3d {path} All Stresses,FullTensor(UCS),Outer Surface")


def create_window(window_name, strain_label, stress_label):
    utils.MetaCommand(f'xyplot create "{window_name}"')
    utils.MetaCommand(f'window active "{window_name}"')
    utils.MetaCommand(f'xyplot frommodel elements "{window_name}" 0 "${{p1}}" Centroid Time all all slabel "{strain_label},Outer Surface"')
    utils.MetaCommand(f'xyplot frommodel elements "{window_name}" 0 "${{p1}}" Centroid Time all all slabel "{stress_label},Outer Surface"')
    utils.MetaCommand('xyplot newreserve 3 0')
    utils.MetaCommand(f'xyplot curve function userdef "User defined" "c1.y" "c2.y" "{window_name}"')
    utils.MetaCommand(f'xyplot axisoptions xlabel set "{window_name}" 0 "{strain_label},Outer Surface"')
    utils.MetaCommand(f'xyplot curve select "{window_name}" "3"')
    utils.MetaCommand(f'xyplot curve set sync axis "{window_name}" selected PointToState')

def main():
    windows = [
        ("Window1", "Strains,Normal-1(UCS)", "Stresses,Normal-1(UCS)"),
        ("Window2", "Strains,Normal-2(UCS)", "Stresses,Normal-2(UCS)"),
        ("Window3", "Strains,Normal-3(UCS)", "Stresses,Normal-3(UCS)"),
        ("Window4", "Strains,Shear-12(UCS)", "Stresses,Shear-12(UCS)"),
        ("Window5", "Strains,Shear-23(UCS)", "Stresses,Shear-23(UCS)"),
        ("Window6", "Strains,Shear-31(UCS)", "Stresses,Shear-31(UCS)")
    ]

    for window_name, strain_label, stress_label in windows:
        create_window(window_name, strain_label, stress_label)
    
    utils.MetaCommand(f'xyplot curve set pointstyle "allwindows" selected 1')
    utils.MetaCommand(f'xyplot curve visible or "allwindows" selected')
    utils.MetaCommand(f'xyplot curve deselect "allwindows" "3"')
    utils.MetaCommand(f'xyplot curve set pointsize "allwindows" selected 10')
    utils.MetaCommand(f'window autotile')


if __name__ == '__main__':
    main()
