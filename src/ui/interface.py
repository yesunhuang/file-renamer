import sys
import os
from src.utils.console_input import safe_input

def display_welcome_message():
    print("\n" + "="*60)
    print("                FILE RENAMER APPLICATION")
    print("="*60)
    print("This application helps you rename multiple files at once.")

def get_user_input(prompt):
    return safe_input(prompt)

def fallback_input():
    # Last resort fallback
    try:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            result = ''
            while True:
                ch = sys.stdin.read(1)
                if ch == '\n' or ch == '\r':
                    print()
                    break
                elif ch == '\b' or ord(ch) == 127:  # backspace or delete
                    if result:
                        result = result[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    result += ch
                    print(ch, end='', flush=True)
            return result
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception:
        # Ultimate fallback if everything fails - return empty string
        print("\nWarning: Input functionality is limited. Using default empty value.")
        return ""

def display_results(results):
    print("Renaming Results:")
    for result in results:
        print(result)

def display_error(message):
    print(f"Error: {message}")

def confirm_action(action):
    """
    Ask user to confirm an action
    
    Args:
        action (str): The action to confirm
        
    Returns:
        bool: True if user confirmed, False otherwise
    """
    response = get_user_input(f"Are you sure you want to {action}? (yes/no): ")
    # Ensure response is not None before calling lower()
    if not response:  # Handles None or empty string
        return False
    return response.lower() in ('yes', 'y')