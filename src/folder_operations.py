'''
Name: 
Description: 
Email: yesunhuang@uchicago.edu
OpenSource: https://github.com/yesunhuang
LastEditors: yesunhuang yesunhuang@uchicago.edu
Msg: 
Author: YesunHuang
Date: 2025-02-27 01:10:48
'''

import os
import shutil

def identify_redundant_folders(directory_path):
    """
    Identify folders that contain exactly one subfolder and no files.
    
    Args:
        directory_path (str): Path to the directory to scan
        
    Returns:
        list: List of tuples (parent_folder_path, child_folder_path)
    """
    redundant_folders = []
    
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return redundant_folders
        
    # Walk through all folders in the directory
    for root, dirs, files in os.walk(directory_path):
        # Skip if this is the root directory itself
        if root == directory_path:
            continue
            
        # Check if this folder contains exactly one subfolder and no files
        if len(dirs) == 1 and len(files) == 0:
            parent_folder = root
            child_folder = os.path.join(root, dirs[0])
            redundant_folders.append((parent_folder, child_folder))
            
    return redundant_folders

def collapse_folder(parent_folder, child_folder):
    """
    Collapse a redundant folder structure by moving the contents of the child folder
    to the parent folder and renaming the parent folder.
    
    Args:
        parent_folder (str): Path to the parent folder
        child_folder (str): Path to the child folder
        
    Returns:
        str: Path to the renamed parent folder if successful, None otherwise
    """
    try:
        parent_name = os.path.basename(parent_folder)
        child_name = os.path.basename(child_folder)
        
        # Create the new folder name by concatenating parent and child names
        new_name = f"{parent_name}_{child_name}"
        parent_dir = os.path.dirname(parent_folder)
        new_path = os.path.join(parent_dir, new_name)
        
        # Check if the new path already exists
        if os.path.exists(new_path):
            # Generate a unique name by adding a suffix
            counter = 1
            while os.path.exists(f"{new_path}_{counter}"):
                counter += 1
            new_path = f"{new_path}_{counter}"
        
        # First, rename the parent folder
        os.rename(parent_folder, new_path)
        
        # Get the updated child folder path after parent was renamed
        updated_child_path = os.path.join(new_path, child_name)
        
        # Move all contents from the child folder to the renamed parent folder
        for item in os.listdir(updated_child_path):
            item_path = os.path.join(updated_child_path, item)
            dest_path = os.path.join(new_path, item)
            
            # If the destination already exists, handle it
            if os.path.exists(dest_path):
                if os.path.isfile(dest_path):
                    os.remove(dest_path)
                elif os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
                    
            # Move the item
            shutil.move(item_path, new_path)
        
        # Remove the empty child folder
        shutil.rmtree(updated_child_path)
        
        return new_path
    except Exception as e:
        print(f"Error collapsing folder: {e}")
        return None

def collapse_redundant_folders(directory_path, recursive=True):
    """
    Identify and collapse all redundant folders in a directory.
    
    Args:
        directory_path (str): Path to the directory to process
        recursive (bool): Whether to recursively process collapsed folders again
        
    Returns:
        list: List of collapsed folder paths
    """
    collapsed_folders = []
    
    # Continue processing until no more redundant folders are found
    # or if not recursive, just do one pass
    while True:
        redundant_folders = identify_redundant_folders(directory_path)
        
        if not redundant_folders:
            break
            
        for parent_folder, child_folder in redundant_folders:
            new_path = collapse_folder(parent_folder, child_folder)
            if new_path:
                collapsed_folders.append(new_path)
                
        if not recursive:
            break
    
    return collapsed_folders

def uncollapse_folder(folder_path):
    """
    Uncollapse a folder by splitting its name at underscores and creating nested folders.
    
    Args:
        folder_path (str): Path to the folder to uncollapse
        
    Returns:
        str: Path to the outermost folder if successful, None otherwise
    """
    try:
        # Skip if the path doesn't exist or isn't a directory
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            print(f"Cannot uncollapse: {folder_path} is not a valid directory")
            return None
            
        folder_name = os.path.basename(folder_path)
        parent_dir = os.path.dirname(folder_path)
        
        # Split the folder name by underscores
        name_parts = folder_name.split('_')
        
        # If there's only one part, nothing to uncollapse
        if len(name_parts) <= 1:
            return folder_path
        
        # Filter out empty parts
        name_parts = [part for part in name_parts if part]
        if not name_parts:
            return folder_path
            
        # Generate unique names for each level to avoid conflicts
        base_folder_name = name_parts[0]
        unique_base_name = base_folder_name
        counter = 1
        while os.path.exists(os.path.join(parent_dir, unique_base_name)) and os.path.join(parent_dir, unique_base_name) != folder_path:
            unique_base_name = f"{base_folder_name}_{counter}"
            counter += 1
            
        # Create a temporary folder for the uncollapsed structure
        temp_path = os.path.join(parent_dir, f"temp_{os.path.basename(folder_path)}_{os.urandom(4).hex()}")
        os.makedirs(temp_path, exist_ok=True)
        
        # Create the nested structure inside the temp path
        current_path = temp_path
        for i, part in enumerate(name_parts):
            new_folder = os.path.join(current_path, part)
            os.makedirs(new_folder, exist_ok=True)
            current_path = new_folder
            
        # The innermost folder is where we'll move all content
        innermost_folder = current_path
        
        # Copy all contents from original folder to the innermost folder
        for item in os.listdir(folder_path):
            source_path = os.path.join(folder_path, item)
            dest_path = os.path.join(innermost_folder, item)
            
            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path)
        
        # Create the actual base folder with the unique name
        target_base_folder = os.path.join(parent_dir, unique_base_name)
        
        # If the folder_path is already the base folder name, we need to move contents out first
        if os.path.basename(folder_path) == unique_base_name:
            # Create a temporary path to hold the original folder's contents
            temp_hold = os.path.join(parent_dir, f"temphold_{os.urandom(4).hex()}")
            os.makedirs(temp_hold, exist_ok=True)
            
            # Move contents to temp hold
            for item in os.listdir(folder_path):
                shutil.move(os.path.join(folder_path, item), os.path.join(temp_hold, item))
                
            # Now remove the original folder and recreate it
            shutil.rmtree(folder_path)
            os.makedirs(target_base_folder, exist_ok=True)
            
            # Move contents back
            for item in os.listdir(temp_hold):
                shutil.move(os.path.join(temp_hold, item), os.path.join(target_base_folder, item))
                
            # Remove temp hold
            shutil.rmtree(temp_hold)
        else:
            # Simply remove the original folder and create the new structure
            shutil.rmtree(folder_path)
            os.makedirs(target_base_folder, exist_ok=True)
        
        # Now copy the structure from temp to the actual location
        current_source = os.path.join(temp_path, name_parts[0])
        current_target = target_base_folder
        
        # For the remaining parts, create each level
        for i in range(1, len(name_parts)):
            next_part = name_parts[i]
            next_source = os.path.join(current_source, next_part)
            next_target = os.path.join(current_target, next_part)
            
            # Create the directory at the target
            os.makedirs(next_target, exist_ok=True)
            
            # Copy all items from the next_source to next_target
            if i == len(name_parts) - 1:  # At the innermost folder
                for item in os.listdir(next_source):
                    source_item = os.path.join(next_source, item)
                    target_item = os.path.join(next_target, item)
                    
                    if os.path.isfile(source_item):
                        shutil.copy2(source_item, target_item)
                    elif os.path.isdir(source_item):
                        shutil.copytree(source_item, target_item)
            
            current_source = next_source
            current_target = next_target
            
        # Finally, remove the temp folder
        shutil.rmtree(temp_path)
        
        # Return the path to the newly created structure
        return target_base_folder
        
    except Exception as e:
        print(f"Error uncollapsing folder: {e}")
        return None

def uncollapse_folders(directory_path, min_parts=2):
    """
    Find and uncollapse folders in a directory based on underscore separators.
    
    Args:
        directory_path (str): Path to the directory to process
        min_parts (int): Minimum number of parts in the name to consider uncollapsing
        
    Returns:
        list: List of uncollapsed folder paths (outermost folders)
    """
    uncollapsed_folders = []
    
    # Skip if the path doesn't exist or isn't a directory
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        return uncollapsed_folders
    
    # Get all immediate subfolders
    folders = [os.path.join(directory_path, item) 
              for item in os.listdir(directory_path) 
              if os.path.isdir(os.path.join(directory_path, item))]
    
    # Process each folder
    for folder in folders:
        folder_name = os.path.basename(folder)
        
        # Check if the folder name has enough parts to uncollapse
        if len(folder_name.split('_')) >= min_parts:
            result = uncollapse_folder(folder)
            if result:
                uncollapsed_folders.append(result)
                
    return uncollapsed_folders
