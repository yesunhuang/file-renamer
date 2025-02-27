'''
Name: 
Description: 
Email: yesunhuang@uchicago.edu
OpenSource: https://github.com/yesunhuang
LastEditors: yesunhuang yesunhuang@uchicago.edu
Msg: 
Author: YesunHuang
Date: 2025-02-26 01:17:01
'''

"""
Entry point script for the File Renamer application.
This simply imports and runs the main function from src/main.py
"""
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main function from src/main.py
from src.main import main

# Run the main function
if __name__ == "__main__":
    main()
