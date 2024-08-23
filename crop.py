import os
from PIL import Image

def find_and_crop_images(folder:str,save:str):
    files = os.listdir(folder)
    filter_images = [f for f in files if f.endswith('right.jpg')]
    
    for image_file in filter_images:
        image_path = os.path.join(folder, image_file)
        
        # 打开图像
        with Image.open(image_path) as img:
            width, height = img.size
            
            cropped_img = img.crop((0, height // 3, width, height))
            
            # 构建保存路径
            # 你可以选择是否要覆盖原图像，或者保存到其他路径
            save_path = os.path.join(save, f"{image_file}")
            cropped_img.save(save_path)
            print(f"Saved cropped image to {save_path}")

# 使用示例
folder = r'd:\Users\ADMIN\Desktop\results\bus'
save = r'd:\Users\ADMIN\Desktop\results\crop_right'
find_and_crop_images(folder,save)
