import os
import sys
import traceback

# Version information
__version__ = '1.1.0'

# Add the parent directory to sys.path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import file operations
try:
    from src.file_operations import rename_files
    from src.rename_utils import remove_prefix_and_order, generate_new_name, find_longest_common_prefix
except ImportError:
    try:
        from file_operations import rename_files
        from rename_utils import remove_prefix_and_order, generate_new_name, find_longest_common_prefix
    except ImportError:
        # Final fallback for direct imports when running from src directory
        import file_operations
        import rename_utils
        rename_files = file_operations.rename_files
        remove_prefix_and_order = rename_utils.remove_prefix_and_order
        generate_new_name = rename_utils.generate_new_name
        find_longest_common_prefix = rename_utils.find_longest_common_prefix

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

def get_items_to_rename(directory_path, include_folders=False):
    """Get list of items (files and optionally folders) to rename"""
    items = []
    if os.path.exists(directory_path):
        for item in os.listdir(directory_path):
            full_path = os.path.join(directory_path, item)
            if os.path.isfile(full_path) or (include_folders and os.path.isdir(full_path)):
                items.append(full_path)
    return items

def run_renaming_operation():
    """Run a single renaming operation"""
    try:
        display_welcome()
        display_version()
        
        # Get user input for the renaming operation
        directory_path = get_user_input("Enter the directory path: ")
        if not directory_path:  # Check for empty input
            print("No directory path provided.")
            return
            
        prefix_format = get_user_input("Enter the prefix format: ")
        # No default prefix format needed - we'll handle empty strings properly
            
        ordering = get_user_input("Enable ordering? (y/n): ")
        if not ordering:  # Handle None or empty string
            ordering = "n"
        ordering = ordering.lower() in ['y', 'yes']
        
        # If no prefix format but ordering is enabled, confirm with user
        if not prefix_format and ordering:
            print("Note: Since no prefix format was specified but ordering is enabled, files will be renamed with just order numbers.")
        
        # Ask if user wants to remove existing prefixes first
        remove_existing_prefixes = get_user_input("Remove existing prefixes and order numbers? (y/n): ")
        if not remove_existing_prefixes:  # Handle None or empty string
            remove_existing_prefixes = "n"
        remove_existing_prefixes = remove_existing_prefixes.lower() in ['y', 'yes']
        
        # Ask if user wants to rename folders as well
        include_folders = get_user_input("Include folders in renaming? (y/n): ")
        if not include_folders:
            include_folders = "n"
        include_folders = include_folders.lower() in ['y', 'yes']
        
        # Get list of items (files and optionally folders) to rename
        items = get_items_to_rename(directory_path, include_folders)
            
        # Show preview of the changes
        if items:
            # Find common prefix if removal is requested
            common_prefix = ""
            if remove_existing_prefixes and items:
                # Get list of basenames for prefix detection
                basenames = [os.path.basename(item) for item in items]
                common_prefix = find_longest_common_prefix(basenames)
                if common_prefix:
                    print(f"Found common prefix: {common_prefix}")
            
            print("\nPreview of changes:")
            renamed_previews = []
            
            for index, item in enumerate(items):
                base_name = os.path.basename(item)
                item_type = "Folder" if os.path.isdir(item) else "File"
                
                # Apply prefix removal if requested
                if remove_existing_prefixes:
                    cleaned_name = remove_prefix_and_order(base_name, common_prefix)
                    intermediate_name = cleaned_name
                else:
                    intermediate_name = base_name
                
                # Generate the new name
                order_value = index + 1 if ordering else None
                new_name = generate_new_name(intermediate_name, prefix_format, order_value)
                renamed_previews.append((item, new_name))
                
                print(f"  {item_type}: {base_name} → {new_name}")
            
            # Ask for confirmation before proceeding
            if confirm_action("proceed with renaming"):
                # If removing prefixes, rename files to clean names first
                if remove_existing_prefixes:
                    temp_items = []
                    for item in items:
                        base_name = os.path.basename(item)
                        dir_name = os.path.dirname(item)
                        
                        cleaned_name = remove_prefix_and_order(base_name, common_prefix)
                        temp_path = os.path.join(dir_name, cleaned_name)
                        
                        # Only rename if the name actually changed
                        if cleaned_name != base_name:
                            # Ensure we don't overwrite existing items
                            if os.path.exists(temp_path) and temp_path != item:
                                if os.path.isfile(temp_path):
                                    print(f"Warning: '{temp_path}' already exists. Will be overwritten.")
                                    os.remove(temp_path)
                                else:
                                    # Can't easily remove directory, so skip
                                    print(f"Warning: Can't rename {base_name} to {cleaned_name} (already exists)")
                                    temp_items.append(item)
                                    continue
                            try:
                                os.rename(item, temp_path)
                                temp_items.append(temp_path)
                            except Exception as e:
                                print(f"Error renaming to clean name: {str(e)}")
                                temp_items.append(item)
                        else:
                            temp_items.append(item)
                    
                    # Use the cleaned items for the next step
                    items = temp_items
                
                # Now apply the new prefix format
                renamed_items = rename_files(items, prefix_format, ordering)
                
                # Display the results of the renaming operation
                results = [f"Renamed: {os.path.basename(old)} → {os.path.basename(new)}" 
                          for old, new in zip(items, renamed_items)]
                display_results(results)
        else:
            print(f"No {'items' if include_folders else 'files'} found in: {directory_path}")
            
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())

def show_main_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("FILE RENAMER MAIN MENU")
    print("="*50)
    print("1. Rename files/folders")
    print("2. Display version information")
    print("3. Exit application")
    print("="*50)
    
    choice = get_user_input("Enter your choice (1-3): ")
    return choice

def main():
    try:
        # Make sure console is visible when running as executable
        ensure_console_visible()
        
        while True:
            choice = show_main_menu()
            
            if choice == "1":
                run_renaming_operation()
            elif choice == "2":
                display_welcome()
                display_version()
                input("Press Enter to continue...")
            elif choice == "3":
                print("Exiting application...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
                
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()