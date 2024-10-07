import os

def clean_path(file_path):
    # Split the path into parts
    path_parts = file_path.split(os.path.sep)
    print(f"Path parts: {path_parts}")  # Debugging line
    count = path_parts.count('Python_project')
    print(f"Count of 'Python_project': {count}")  # Debugging line

    # If 'Python_project' appears more than once, clean the path
    if count > 1:
        cleaned_parts = []
        for part in path_parts:
            if part == 'Python_project' and count > 1:
                count -= 1  # Reduce the count for removal
                print(f"Removing 'Python_project', remaining count: {count}")  # Debugging line
            else:
                cleaned_parts.append(part)  # Keep the rest of the path

        # Reconstruct the cleaned path
        cleaned_path = os.path.sep.join(cleaned_parts)
        return cleaned_path
    return file_path  # Return the original path if it's correct

# Example usage
original_path = r"C:\Users\nelly\Desktop\projet python\python_project\Python_project\muxic\RERD.mp3"
cleaned_path = clean_path(original_path)

print(f"Original: {original_path}")
print(f"Cleaned: {cleaned_path}")
