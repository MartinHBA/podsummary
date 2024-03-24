import os

# Path to the file
file_path = 'workload/Elektronické_voľby_sú_hlúposť,_odhadneme_víťaza_(22._3._2024).wav'

# Check if the file exists
if os.path.exists(file_path):
    print(f"File found: {file_path}")
else:
    print(f"File not found: {file_path}")

# Print the current working directory
print(f"Current Working Directory: {os.getcwd()}")
