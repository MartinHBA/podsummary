import requests
import time

def check_job_status_and_download_results(job_url, subscription_key, output_file_path):
    """
    Checks the status of the transcription job and downloads the results
    when the job is completed. Saves the transcription text to a specified file.

    Parameters:
    - job_url: The URL to check the job status, obtained from the job submission response.
    - subscription_key: Your Azure Speech Service subscription key.
    - output_file_path: Path to the file where the transcription results will be saved.
    """
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    while True:
        # Check the status of the transcription job
        response = requests.get(job_url, headers=headers)
        job_status = response.json()

        print("Checking job status...")
        if job_status['status'] in ['Succeeded', 'Failed']:
            print(f"Job status: {job_status['status']}")
            break
        else:
            print("Job is not yet completed. Waiting...")
            time.sleep(30)  # Wait for 30 seconds before checking again

    # If the job succeeded, download the results
    if job_status['status'] == 'Succeeded':
        files_url = job_status['links']['files']
        files_response = requests.get(files_url, headers=headers)
        files = files_response.json()

        transcriptions = []  # Initialize a list to hold all transcription texts

        for file in files['values']:
            if file['kind'] == 'Transcription':
                transcription_url = file['links']['contentUrl']
                transcription_response = requests.get(transcription_url)
                transcription_text = transcription_response.json()

                # Extract the display text from the best confidence result
                for result in transcription_text['recognizedPhrases']:
                    display_text = result['nBest'][0]['display']
                    transcriptions.append(display_text)

        # Save the transcription texts to a file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for text in transcriptions:
                f.write(text + '\n')
        print(f"Transcription saved to {output_file_path}")
    elif job_status['status'] == 'Failed':
        print("Transcription job failed. No results to download.")

