import os
import shutil
from src.rename_utils import generate_new_name

def rename_files(file_paths, prefix_format, use_order=False):
    """
    Rename files or folders using the specified prefix format.
    
    Args:
        file_paths (list): List of file or folder paths to rename
        prefix_format (str): Format string for the new names
        use_order (bool): Whether to include order numbers
        
    Returns:
        list: List of new file paths
    """
    new_paths = []
    
    for i, path in enumerate(file_paths):
        if not os.path.exists(path):
            print(f"Warning: Path does not exist: {path}")
            new_paths.append(path)  # Keep original path in result
            continue
            
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        
        # Generate new name with or without order number
        order_value = i + 1 if use_order else None
        new_name = generate_new_name(filename, prefix_format, order_value)
        
        # Create the new path
        new_path = os.path.join(directory, new_name)
        
        # Handle name collision
        if os.path.exists(new_path) and new_path != path:
            print(f"Warning: '{new_name}' already exists. Skipping rename for '{filename}'")
            new_paths.append(path)  # Keep original path in result
            continue
            
        try:
            os.rename(path, new_path)
            new_paths.append(new_path)
        except Exception as e:
            print(f"Error renaming '{filename}' to '{new_name}': {str(e)}")
            new_paths.append(path)  # Keep original path in result
            
    return new_paths

def move_files(file_list, destination_folder):
    moved_files = []
    for file in file_list:
        shutil.move(file, destination_folder)
        moved_files.append(os.path.join(destination_folder, os.path.basename(file)))
    return moved_files

def check_file_existence(file_path):
    return os.path.exists(file_path)