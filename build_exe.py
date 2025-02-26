import sys
import os
import shutil
import subprocess
import pkg_resources

def check_and_remove_pathlib():
    """Check if pathlib is installed as a package and remove it if needed"""
    try:
        # Check if pathlib is installed as a package
        pathlib_dist = pkg_resources.get_distribution('pathlib')
        
        # If we get here, pathlib is installed as a package
        print("Detected obsolete pathlib package. Removing it before building...")
        
        # Use subprocess to run pip uninstall
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "pathlib"])
        
        print("Successfully removed pathlib package.")
    except pkg_resources.DistributionNotFound:
        # pathlib not installed as a package, which is good
        pass
    except Exception as e:
        print(f"Warning: Failed to remove pathlib package: {e}")
        print("You may need to manually uninstall it with: pip uninstall pathlib")

# Clean up any previous builds
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")

# Check for and remove pathlib if it exists as a package
check_and_remove_pathlib()

print("Building File Renamer executable...")

try:
    import PyInstaller.__main__
    
    PyInstaller.__main__.run([
        'run.py',                         # Use run.py as the entry point
        '--name=FileRenamer',             # Name of the executable
        '--onefile',                      # Create a single executable file
        # '--add-data=config;config',      # Include the config directory if it exists
        # '--icon=config/icon.ico',        # Include an icon if you have one
        # '--noconsole',                   # REMOVED: We need the console window to be visible
        '--clean',                        # Clean PyInstaller cache
    ])
    
    print("Build complete! Executable is in the 'dist' folder.")
except Exception as e:
    print(f"Error during build: {e}")
    sys.exit(1)