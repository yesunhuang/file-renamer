import os
import sys
import traceback

# Version information
__version__ = '1.2.0'

# Add the parent directory to sys.path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import file operations
try:
    from src.file_operations import rename_files
    from src.rename_utils import remove_prefix_and_order, generate_new_name
except ImportError:
    try:
        from file_operations import rename_files
        from rename_utils import remove_prefix_and_order, generate_new_name
    except ImportError:
        # Final fallback for direct imports when running from src directory
        import file_operations
        import rename_utils
        rename_files = file_operations.rename_files
        remove_prefix_and_order = rename_utils.remove_prefix_and_order
        generate_new_name = rename_utils.generate_new_name

# Import UI components
try:
    from src.ui.interface import display_welcome_message as display_welcome, get_user_input, display_results, confirm_action
except ImportError:
    try:
        from ui.interface import display_welcome_message as display_welcome, get_user_input, display_results, confirm_action
    except ImportError:
        # Final fallback for direct imports
        from interface import display_welcome_message as display_welcome, get_user_input, display_results, confirm_action

def display_version():
    """Display the current version of the application"""
    print(f"File Renamer v{__version__}")

def ensure_console_visible():
    """Ensure the console window is visible when running as an exe"""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        if os.name == 'nt':  # Windows
            try:
                import ctypes
                ctypes.windll.kernel32.AllocConsole()
                sys.stdin = open('CONIN$', 'r')
                sys.stdout = open('CONOUT$', 'w')
                sys.stderr = open('CONOUT$', 'w')
                print("Console window allocated successfully")
            except Exception as e:
                print(f"Failed to allocate console: {e}")

def main():
    try:
        # Make sure console is visible when running as executable
        ensure_console_visible()
        
        display_welcome()
        display_version()
        
        # Get user input for the renaming operation
        directory_path = get_user_input("Enter the directory path: ")
        if not directory_path:  # Check for empty input
            print("No directory path provided.")
            input("Press Enter to exit...")
            return
            
        prefix_format = get_user_input("Enter the prefix format: ")
        if not prefix_format:  # Check for empty pattern
            prefix_format = "file_{num}"  # Default pattern if none provided
            print(f"Using default prefix format: {prefix_format}")
            
        ordering = get_user_input("Enable ordering? (y/n): ")
        if not ordering:  # Handle None or empty string
            ordering = "n"
        ordering = ordering.lower() in ['y', 'yes']
        
        # Ask if user wants to remove existing prefixes first
        remove_existing_prefixes = get_user_input("Remove existing prefixes and order numbers? (y/n): ")
        if not remove_existing_prefixes:  # Handle None or empty string
            remove_existing_prefixes = "n"
        remove_existing_prefixes = remove_existing_prefixes.lower() in ['y', 'yes']
        
        # Get list of files in directory
        if os.path.exists(directory_path):
            files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) 
                    if os.path.isfile(os.path.join(directory_path, f))]
            
            # Show preview of the changes
            if files:
                print("\nPreview of changes:")
                for index, file in enumerate(files):
                    base_name = os.path.basename(file)
                    
                    # Apply prefix removal if requested
                    if remove_existing_prefixes:
                        cleaned_name = remove_prefix_and_order(base_name)
                        intermediate_name = cleaned_name
                    else:
                        intermediate_name = base_name
                    
                    # Generate the new name
                    order_value = index + 1 if ordering else None
                    new_name = generate_new_name(intermediate_name, prefix_format, order_value)
                    
                    print(f"  {base_name} → {new_name}")
                
                # Ask for confirmation before proceeding
                if confirm_action("proceed with renaming"):
                    # If removing prefixes, rename files to clean names first
                    if remove_existing_prefixes:
                        temp_files = []
                        for file in files:
                            base_name = os.path.basename(file)
                            dir_name = os.path.dirname(file)
                            cleaned_name = remove_prefix_and_order(base_name)
                            temp_path = os.path.join(dir_name, cleaned_name)
                            
                            # Only rename if the name actually changed
                            if cleaned_name != base_name:
                                # Remove target if it exists already
                                if os.path.exists(temp_path):
                                    os.remove(temp_path)
                                os.rename(file, temp_path)
                                temp_files.append(temp_path)
                            else:
                                temp_files.append(file)
                        
                        # Use the cleaned files for the next step
                        files = temp_files
                    
                    # Now apply the new prefix format
                    renamed_files = rename_files(files, prefix_format, ordering)
                    
                    # Display the results of the renaming operation
                    results = [f"Renamed: {os.path.basename(old)} → {os.path.basename(new)}" 
                              for old, new in zip(files, renamed_files)]
                    display_results(results)
        else:
            print(f"Directory not found: {directory_path}")
            
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())
        
    # Always wait for user input before exiting
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()