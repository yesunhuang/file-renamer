import sys
import os
import shutil
import subprocess
import pkg_resources
import PyInstaller.__main__

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

def build_executable():
    """Build the executable with PyInstaller"""
    
    # Ensure the dist directory exists
    if not os.path.exists('dist'):
        os.makedirs('dist')
        
    # Define icon path - create this file in the project root
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file_renamer_icon.ico')
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run_script_path = os.path.join(script_dir, 'run.py')
    src_path = os.path.join(script_dir, 'src')
    
    # PyInstaller command line arguments
    args = [
        run_script_path,             # Script to convert
        '--onefile',                 # Create a single executable
        '--name=FileRenamer',        # Name of the executable
        '--noconsole',               # Hide console window
        f'--icon={icon_path}',       # Add application icon
        '--clean',                   # Clean PyInstaller cache
        f'--add-data={src_path};src', # Include the src directory
        f'--add-data={icon_path};.',   # Include the icon file
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("Executable built successfully!")

if __name__ == "__main__":
    build_executable()