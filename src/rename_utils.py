import re
import os

def generate_new_name(original_name, prefix_format, order=None):
    """
    Generate a new name for a file or folder based on the original name,
    user-defined prefix format, and specified order.
    """
    # Extract the base name and extension
    base_name, extension = original_name.rsplit('.', 1) if '.' in original_name else (original_name, '')
    
    # Apply the prefix format to get prefixed name
    if not prefix_format:
        prefixed_name = base_name
    else:
        # If the prefix already ends with underscore, don't add another
        if prefix_format.endswith('_'):
            prefixed_name = f"{prefix_format}"
        else:
            prefixed_name = f"{prefix_format}_"
            
    # Insert order between prefix and base name if specified
    if order:
        new_name = f"{prefixed_name}{order}_{base_name}"
    else:
        new_name = f"{prefixed_name}{base_name}"
    
    # Reattach the extension if it exists
    if extension:
        new_name += f".{extension}"
    
    return new_name

def apply_prefix_format(base_name, prefix_format):
    """
    Apply the user-defined prefix format to the base name.
    """
    if not prefix_format:
        return base_name
    
    # If the prefix_format contains a placeholder {}, format it
    if '{}' in prefix_format:
        return prefix_format.format(base_name)
    
    # Check if prefix already ends with underscore
    if prefix_format.endswith('_'):
        return f"{prefix_format}{base_name}"
    else:
        # Otherwise, concatenate with an underscore
        return f"{prefix_format}_{base_name}"

def find_longest_common_prefix(filenames):
    """
    Find the longest common prefix across multiple filenames.
    """
    if not filenames:
        return ""
    
    # Get only basenames without paths
    basenames = [os.path.basename(f) for f in filenames]
    
    # Find the shortest filename to avoid index errors
    min_length = min(len(name) for name in basenames)
    
    # Find the common prefix
    prefix_end = 0
    for i in range(min_length):
        char = basenames[0][i]
        if all(name[i] == char for name in basenames):
            prefix_end = i + 1
        else:
            break
    
    # Get the common prefix
    common_prefix = basenames[0][:prefix_end]
    
    # Make sure we don't break in the middle of a word/segment
    # Find the last underscore in the common prefix
    last_underscore = common_prefix.rfind('_')
    if last_underscore > 0:
        common_prefix = common_prefix[:last_underscore+1]  # Keep the underscore
    
    return common_prefix

def remove_prefix_and_order(filename, common_prefix=None, file_list=None):
    """
    Remove existing prefix and order numbers from a filename.
    Also handles duplicate patterns in filenames.
    """
    # Extract the base name and extension
    base_name, extension = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    
    # If we have a common prefix from a file list, use that
    if common_prefix is None and file_list is not None and len(file_list) > 1:
        common_prefix = find_longest_common_prefix(file_list)
    
    # Check for duplicated patterns in the filename (like "name_name")
    # Find potential duplicate patterns
    for i in range(len(base_name) // 2):
        half_length = len(base_name) // 2
        if base_name[:half_length] == base_name[half_length:2*half_length]:
            base_name = base_name[:half_length]
            break
    
    # Clean the base name - use a more comprehensive approach
    # First, remove any known common prefix
    if common_prefix and base_name.startswith(common_prefix):
        base_name = base_name[len(common_prefix):]
        
    # Next, use a regex to remove common prefixes followed by underscore
    common_prefixes = ['img', 'doc', 'file', 'photo', 'pic', 'renamed', '2025', '2024']
    prefix_pattern = r'^(?:' + '|'.join(common_prefixes) + r')_'
    base_name = re.sub(prefix_pattern, '', base_name, flags=re.IGNORECASE)
    
    # Repeatedly remove order numbers (pattern: digits followed by underscore) 
    # from the beginning until no more matches found
    old_base_name = ""
    while old_base_name != base_name:
        old_base_name = base_name
        base_name = re.sub(r'^(\d+)_', '', base_name)
    
    # Remove any remaining leading/trailing underscores
    base_name = base_name.strip('_')
    
    # Remove duplicate content in filename (e.g., word_word)
    tokens = base_name.split('_')
    unique_tokens = []
    for token in tokens:
        if token not in unique_tokens:
            unique_tokens.append(token)
    
    # Reconstruct base_name with unique tokens
    base_name = '_'.join(unique_tokens)
    
    # Reattach the extension if it exists
    if extension:
        cleaned_name = f"{base_name}.{extension}"
    else:
        cleaned_name = base_name
        
    return cleaned_name