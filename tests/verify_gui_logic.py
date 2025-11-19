import os
import shutil
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from folder_operations import identify_redundant_folders, collapse_redundant_folders, uncollapse_folders, uncollapse_folder

def setup_test_env():
    base_dir = "test_folder_ops"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)
    return base_dir

def test_collapse_logic():
    print("Testing Collapse Logic...")
    base_dir = setup_test_env()
    
    # Create redundant structure: parent/child/file.txt
    parent = os.path.join(base_dir, "parent")
    child = os.path.join(parent, "child")
    os.makedirs(child)
    with open(os.path.join(child, "file.txt"), "w") as f:
        f.write("content")
        
    # Identify
    redundant = identify_redundant_folders(base_dir)
    print(f"Identified: {redundant}")
    if not redundant:
        print("FAIL: Did not identify redundant folder")
        return

    # Collapse
    collapsed = collapse_redundant_folders(base_dir, recursive=True)
    print(f"Collapsed: {collapsed}")
    
    expected_path = os.path.join(base_dir, "parent_child")
    if os.path.exists(expected_path) and os.path.exists(os.path.join(expected_path, "file.txt")):
        print("PASS: Collapse successful")
    else:
        print("FAIL: Collapse failed")
        
    # Cleanup
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

def test_uncollapse_logic():
    print("\nTesting Uncollapse Logic...")
    base_dir = setup_test_env()
    
    # Create collapsed structure: parent_child/file.txt
    collapsed_folder = os.path.join(base_dir, "parent_child")
    os.makedirs(collapsed_folder)
    with open(os.path.join(collapsed_folder, "file.txt"), "w") as f:
        f.write("content")
        
    # Uncollapse
    uncollapsed = uncollapse_folders(base_dir, min_parts=2)
    print(f"Uncollapsed: {uncollapsed}")
    
    expected_parent = os.path.join(base_dir, "parent")
    expected_child = os.path.join(expected_parent, "child")
    
    if os.path.exists(expected_child) and os.path.exists(os.path.join(expected_child, "file.txt")):
        print("PASS: Uncollapse successful")
    else:
        print("FAIL: Uncollapse failed")

    # Cleanup
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

if __name__ == "__main__":
    test_collapse_logic()
    test_uncollapse_logic()
