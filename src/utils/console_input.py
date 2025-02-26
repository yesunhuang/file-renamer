import os
import sys

def safe_input(prompt=""):
    """
    A cross-platform safe input function that works even when sys.stdin is unavailable.
    Used as a fallback when standard input() fails, particularly in packaged executables.
    
    Args:
        prompt (str): The prompt to display to the user
        
    Returns:
        str: The user's input (empty string if input fails)
    """
    print(prompt, end='', flush=True)
    
    # Try standard input first
    try:
        return input() or ""  # Return empty string if input() returns None
    except Exception:
        pass
        
    # Windows-specific implementation
    if os.name == 'nt':
        try:
            import msvcrt
            result = ''
            while True:
                char = msvcrt.getwch()
                if char == '\r':  # Enter key
                    print()  # Move to next line
                    return result
                elif char == '\b':  # Backspace
                    if result:
                        result = result[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    result += char
                    print(char, end='', flush=True)
        except ImportError:
            pass
    
    # Unix-like systems implementation
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
                # FIX: The condition was incorrectly evaluating to always True
                # because "or '\r'" is always True
                if ch == '\n' or ch == '\r':  # Corrected condition
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
        # Ultimate fallback - return empty string instead of None
        print("\nWarning: Input functionality is limited. Using default empty value.")
        return ""
