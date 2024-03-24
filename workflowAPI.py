from takewav import download_newest_episode, convert_mp3_to_wav
from uploadToBlob import upload_file_to_blob_and_generate_sas
from utils.helpers import get_secret_from_key_vault, read_text_file
from utils.cleanupFiles import delete_files
from analyzewav import submit_batch_transcription
from checkJob import check_job_status_and_download_results
from gpt import summarize_text_with_chatgpt
import logging


def process_new_episode():
    # Set vault URL and other constants
    vault_url = "https://vault57765.vault.azure.net/"  
    feed_url = 'https://anchor.fm/s/8a651488/podcast/rss'
    account_name = 'speech355'
    container_name = 'workload'
    service_region = 'westeurope'

    try:
        # Download the newest episode as mp3
        filename = download_newest_episode(feed_url)

        # Convert it to wav
        wavfile = filename.replace("mp3", "wav")
        convert_mp3_to_wav("workload/" + filename, "workload/" + wavfile)

        # Prepare storage account details
        account_key = get_secret_from_key_vault(vault_url, "storagekey")
        blob_name = wavfile
        file_path = "workload/" + wavfile

        # Upload to Blob and generate SAS URL
        sas_url = upload_file_to_blob_and_generate_sas(account_name, account_key, container_name, blob_name, file_path)
        
        # Cleanup local files
        delete_files(filename, wavfile)

        # Submit batch transcription
        subscription_key = get_secret_from_key_vault(vault_url, "speechkey")
        self_url = submit_batch_transcription(sas_url, subscription_key, service_region)
        
        if not self_url:
            raise ValueError("Failed to submit the job or extract 'self' URL.")

        # Check if transcription completed and download results
        output_file_path = 'workload/transcription_result.txt'
        check_job_status_and_download_results(self_url, subscription_key, output_file_path)

        # Analyze the transcription result
        api_key = get_secret_from_key_vault(vault_url, "gptapi")
        text_content = read_text_file(output_file_path)
        summary = summarize_text_with_chatgpt(text_content, api_key)

        if summary:
            # Saving the summary to a file
            with open('workload/response.txt', 'w', encoding='utf-8') as file:
                file.write(summary)
            # Log success or take other actions as needed
            logging.info("Episode processing completed successfully.")
        else:
            # Log the absence of a summary or take other actions
            logging.warning("No summary was returned.")

    except Exception as e:
        # Log any exceptions that occurred during processing
        logging.error(f"An error occurred during episode processing: {str(e)}")
