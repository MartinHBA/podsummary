import requests
from utils.helpers import get_secret_from_key_vault

# Function to read the text file content
#def read_text_file(file_path):
#    with open(file_path, 'r', encoding='utf-8') as file:
#        return file.read()

# Function to summarize the text using ChatGPT API
def summarize_text_with_chatgpt(text, api_key):
    url = "https://api.openai.com/v1/chat/completions"  # Use the correct endpoint for ChatGPT
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-3.5-turbo",  # Adjust model as needed
        "messages": [{"role": "system", "content": "Summarize the following podcast transcript in Slovak in bullet points, do not mention ads if any, do not summarize anything menitoned in short news block at beginning, do not mention closing segment about authors etc.:"},
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


