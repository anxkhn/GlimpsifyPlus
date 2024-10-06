import os
import shutil

def delete_empty_directories(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                
def delete_directories_with_mp4(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            mp4_files = [file for file in os.listdir(dir_path) if file.endswith('.mp4')]
            if len(mp4_files) == len(os.listdir(dir_path)):
                # os.rmdir(dir_path)
                shutil.rmtree(dir_path)

def delete_directories_without_keyword(directory, keyword):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not keyword in dir:
                shutil.rmtree(dir_path)

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory) 

if __name__ == '__main__':
    # Example usage
    directory_path = 'data'
    delete_empty_directories(directory_path)
    delete_directories_with_mp4(directory_path)
    delete_directories_without_keyword(directory_path, '_peak_frames')
