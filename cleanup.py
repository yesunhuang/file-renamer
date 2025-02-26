'''
Name: 
Description: 
Email: yesunhuang@uchicago.edu
OpenSource: https://github.com/yesunhuang
LastEditors: yesunhuang yesunhuang@uchicago.edu
Msg: 
Author: YesunHuang
Date: 2025-02-26 01:22:44
'''

"""
Script to clean up unnecessary files from the repository
"""
import os
import shutil

def cleanup_repo():
    """Remove unnecessary files and directories"""
    dirs_to_remove = [
        '__pycache__',
        'build',
        'dist',
        '.pytest_cache',
        '.coverage',
        '.mypy_cache',
        '.eggs'
    ]
    
    files_to_remove = [
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.DS_Store',
        '.coverage',
        '*.spec',
        '*.log',
        '*.tmp'
    ]
    
    # Walk through the directory tree
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
            
        # Remove directories
        for d in dirs[:]:  # Make a copy since we'll modify dirs
            for pattern in dirs_to_remove:
                if d == pattern or (pattern.startswith('*') and d.endswith(pattern[1:])):
                    try:
                        print(f"Removing directory: {os.path.join(root, d)}")
                        shutil.rmtree(os.path.join(root, d))
                        dirs.remove(d)  # Don't recurse into this directory
                        break
                    except Exception as e:
                        print(f"Error removing {os.path.join(root, d)}: {e}")
        
        # Remove files
        for f in files:
            for pattern in files_to_remove:
                if pattern == f or (pattern.startswith('*') and f.endswith(pattern[1:])):
                    try:
                        print(f"Removing file: {os.path.join(root, f)}")
                        os.remove(os.path.join(root, f))
                        break
                    except Exception as e:
                        print(f"Error removing {os.path.join(root, f)}: {e}")

if __name__ == "__main__":
    cleanup_repo()
    print("Repository cleanup complete!")
