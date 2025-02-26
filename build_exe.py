import PyInstaller.__main__
import os
import shutil

# Clean up any previous builds
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")

print("Building File Renamer executable...")

PyInstaller.__main__.run([
    'run.py',                         # Use run.py as the entry point
    '--name=FileRenamer',             # Name of the executable
    '--onefile',                      # Create a single executable file
    '--add-data=config;config',       # Include the config directory
    '--icon=config/icon.ico',         # Optional: include an icon if you have one
    # '--noconsole',                  # REMOVED: We need the console window to be visible
    '--clean',                        # Clean PyInstaller cache
])

print("Build complete! Executable is in the 'dist' folder.")