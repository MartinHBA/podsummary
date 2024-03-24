import os

def delete_files(filename, wavfile):
    # Assuming `filename` and `wavfile` are the complete names including extensions
    files_to_delete = ["workload/" + filename, "workload/" + wavfile]

    for file_to_delete in files_to_delete:
        try:
            os.remove(file_to_delete)
            print(f"Deleted file: {file_to_delete}")
        except FileNotFoundError:
            print(f"File not found: {file_to_delete}")
        except Exception as e:
            print(f"Error deleting file {file_to_delete}: {e}")
