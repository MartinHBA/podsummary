import requests
from utils.helpers import get_secret_from_key_vault

def submit_batch_transcription(sas_url, subscription_key, service_region):
    """
    Submits a batch transcription job to Azure's Speech Service and returns the 'self' URL.

    Parameters:
    - sas_url: The SAS URL to the audio file in Azure Blob Storage.
    - subscription_key: Your Azure Speech Service subscription key.
    - service_region: Your Azure Speech Service region.

    Returns:
    - The 'self' HTTPS URL if successful, None otherwise.
    """
    endpoint = f"https://{service_region}.cris.ai/api/speechtotext/v3.0/transcriptions"

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    }

    body = {
        "contentUrls": [sas_url],
        "properties": {
            "diarizationEnabled": False,
            "wordLevelTimestampsEnabled": False,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked"
        },
        "locale": "sk-SK",
        "displayName": "Batch Transcription Example"
    }

    response = requests.post(endpoint, headers=headers, json=body)
    
    # Adjusted to accept both 201 and 202 status codes
    if response.status_code in [201, 202]:
        response_json = response.json()
        self_url = response_json.get('self', None)
        if self_url:
            print("Transcription job submitted successfully.")
            return self_url
        else:
            print("Failed to find 'self' URL in the response.")
            return None
    else:
        print("Failed to submit transcription job. Response code:", response.status_code)
        print("Response:", response.text)
        return None


