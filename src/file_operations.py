import os
import shutil
try:
    from src.rename_utils import generate_new_name
except ImportError:
    from rename_utils import generate_new_name

def rename_files(file_list, prefix_format, ordering=None):
    renamed_files = []
    for index, file in enumerate(file_list):
        # Generate new name for the file
        order_value = index + 1 if ordering else None
        base_name = os.path.basename(file)
        new_name = generate_new_name(base_name, prefix_format, order_value)
        
        # Create full path for new file
        dir_name = os.path.dirname(file)
        new_path = os.path.join(dir_name, new_name)
        
        # Check if the target file already exists and remove it
        if os.path.exists(new_path):
            os.remove(new_path)
            
        # Rename the file
        os.rename(file, new_path)
        renamed_files.append(new_path)
    return renamed_files

def move_files(file_list, destination_folder):
    moved_files = []
    for file in file_list:
        shutil.move(file, destination_folder)
        moved_files.append(os.path.join(destination_folder, os.path.basename(file)))
    return moved_files

def check_file_existence(file_path):
    return os.path.exists(file_path)