import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gpt import summarize_text_with_chatgpt
from utils.helpers import get_secret_from_key_vault

# Function to read the text file content
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Example usage
api_key= get_secret_from_key_vault("https://vault57765.vault.azure.net/", "gptapi")

file_path = os.path.abspath("workload/transcription_result.txt")
print(f"Attempting to access file at: {file_path}")
text_content = read_text_file(file_path)

text_content = read_text_file("workload/transcription_result.txt")
summary = summarize_text_with_chatgpt(text_content, api_key)

# Example usage continued from the previous code
if summary:
    print("Summary in Slovak (in bullet points):", summary)
    # Saving the summary to a file
    with open('response.txt', 'w', encoding='utf-8') as file:
        file.write(summary)
    print("Summary saved to response.txt")
else:
    print("No summary was returned.")


