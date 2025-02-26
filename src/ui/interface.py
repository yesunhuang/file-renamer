def display_welcome_message():
    print("Welcome to the File Renamer Application!")

def get_user_input(prompt):
    return input(prompt)

def display_results(results):
    print("Renaming Results:")
    for result in results:
        print(result)

def display_error(message):
    print(f"Error: {message}")

def confirm_action(action):
    return get_user_input(f"Are you sure you want to {action}? (yes/no): ").lower() == 'yes'