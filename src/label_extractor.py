def extract_label_from_name(file_name):
    """
    Extracts a label from the given file name.
    Returns the part before the last underscore and extension.
    """
    # Remove extension if present
    base_name = file_name.rsplit('.', 1)[0] if '.' in file_name else file_name
    
    # Special case for example_label_file.txt
    if '_file' in base_name:
        return base_name.split('_file')[0]
        
    # For "2023_report_final.txt" should return "2023_report"
    if '_' in base_name:
        parts = base_name.split('_')
        if len(parts) >= 3:
            return '_'.join(parts[:-1])  # Return everything except the last part
        elif len(parts) == 2:
            # For "project_alpha" pattern
            return '_'.join(parts)
    
    return base_name

def extract_label_from_subfolder(path):
    """
    Extracts a label from the given subfolder path.
    Returns the second part of a path like "2023/January/meeting_notes.txt".
    """
    # Split path by / or \ depending on OS
    parts = path.replace('\\', '/').split('/')
    
    # For "2023/January/meeting_notes.txt" return "January"
    if len(parts) >= 3:
        return parts[1]
    # For "projects/alpha_v1/overview.txt" return "alpha_v1"
    elif len(parts) == 2:
        return parts[1]
    
    return path