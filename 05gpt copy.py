import requests
from utils.helpers import get_secret_from_key_vault

# Function to read the text file content
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to summarize the text using ChatGPT API
def summarize_text_with_chatgpt(text, api_key):
    url = "https://api.openai.com/v1/chat/completions"  # Use the correct endpoint for ChatGPT
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-3.5-turbo",  # Adjust model as needed
        "messages": [{"role": "system", "content": "3 most interesting things on this text mentioned in Slovak in bullet points:"},
                     {"role": "user", "content": text}],
        "temperature": 0.7,
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # Extracting the text from the response
        response_data = response.json()
        summary = response_data['choices'][0]['message']['content']
        return summary
    else:
        print(f"Failed to get summary. Status code: {response.status_code}")
        return None



# prepare vault and secret
vault_url = "https://vault57765.vault.azure.net/"  # Replace with your Key Vault URL
secret_name = "gptapi"  # Replace with your secret name

# Example usage
api_key= get_secret_from_key_vault(vault_url, secret_name)
file_path = "transcription_result.txt"  # Your transcription text file
text_content = read_text_file(file_path)
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

