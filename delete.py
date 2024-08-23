import os
import datetime

def subdirs_in_path(path:str):
    contents = os.listdir(path) # all files + directors in total
    subdirs = [f for f in contents if os.path.isdir(os.path.join(path, f))] # pick directors in total
    return subdirs



if __name__ == "__main__":

    folder_path = r'Z:\cae_jobs\sb'
    subdirs = subdirs_in_path(folder_path)

    date_to_delete = datetime.date(2024, 8, 23)

    for subdir in subdirs:
        s_path = os.path.join(folder_path,subdir)
        cars = subdirs_in_path(s_path)
        for car in cars:
            path = os.path.join(s_path,car)
            
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                
                if filename.endswith('.png') and not filename.startswith('isometric'):
                    creation_time = datetime.date.fromtimestamp(os.path.getmtime(file_path))

                    if creation_time == date_to_delete:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
        

