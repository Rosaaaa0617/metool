from PIL import Image
import os, shutil


def subdirs_in_path(path:str):
    contents = os.listdir(path) # all files + directors in total
    subdirs = [f for f in contents if os.path.isdir(os.path.join(path, f))] # pick directors in total
    return subdirs

def all_in_one(dir, name, view:str):
    folder_path = os.path.join(dir,name)
    state_keywords = ['state0', 'state3', 'state5']
    image_files = [f for f in os.listdir(folder_path) if f.startswith(view) and any(keyword in f for keyword in state_keywords)]
    image_files.sort()
    
    first_image = Image.open(os.path.join(folder_path, image_files[0]))
    width = first_image.width
    height = first_image.height

    total_width = width * len(image_files)
    combined_image = Image.new('RGB', (total_width, height))

    x_offset = 0
    for image_file in image_files:
        img = Image.open(os.path.join(folder_path, image_file))
        combined_image.paste(img, (x_offset, 0))
        x_offset += width

    output_path = os.path.join(dir,f"{name}_{view}.jpg")
    remove_file(output_path)
    combined_image.save(output_path)

    print(f'saved {output_path}')
    
def remove_file(file):
    if  os.path.exists(file):
        os.remove(file)
        print(f'exist {file} and delete')

if __name__ == "__main__":
    os.system('cls') 
    #-----------------------------
    # car_dir = 'smallcar'
    # car_dir = 'bus'
    # car_dir = 'truck'
    #-----------------------------
    # results = r'd:/Users/ADMIN/Desktop/results'
    results = r'z:/cae_jobs/results'
    car_dirs = subdirs_in_path(results)
    # car_dirs = ['bus']
    for car_dir in car_dirs:
        dir = os.path.join(results,car_dir)
        subdirs = subdirs_in_path(dir)
        
        for name in subdirs:
            views = ['top', 'front', 'right', 'left']
            for view in views:
                all_in_one(dir, name, view)
        
