import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.cleanupFiles import delete_files




def get_first_two_files(folder_path):
    # List all files in the given folder
    try:
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    except FileNotFoundError:
        print(f"The folder '{folder_path}' was not found.")
        return None, None
    
    # Initialize the file variables
    file1, file2 = None, None

    # Check if there are at least two files in the folder
    if len(files) >= 2:
        file1, file2 = files[0], files[1]
    else:
        print("Less than two files were found in the folder.")
    
    return file1, file2

# Example usage

folder_path = "M:/git/podsummary/workload"
file1, file2 = get_first_two_files(folder_path)

print(f"File 1: {file1}")
print(f"File 2: {file2}")


# cleanup files commented out
delete_files(file1, file2)
