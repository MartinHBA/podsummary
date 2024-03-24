from takewav import download_newest_episode
from takewav import convert_mp3_to_wav

from uploadToBlob import upload_file_to_blob_and_generate_sas
from utils.helpers import get_secret_from_key_vault

from utils.cleanupFiles import delete_files

from analyzewav import submit_batch_transcription

from checkJob import check_job_status_and_download_results

from gpt import summarize_text_with_chatgpt
from utils.helpers import read_text_file

# set vault url
vault_url = "https://vault57765.vault.azure.net/"  

# RSS feed URL
feed_url = 'https://anchor.fm/s/8a651488/podcast/rss'

# Download the newest episode as mp3
filename = download_newest_episode(feed_url)

# Convert it to wav
wavfile = filename.replace("mp3", "wav")
convert_mp3_to_wav("workload/" + filename, "workload/" + wavfile)


# prepare storage account details
account_name = 'speech355'
account_key = get_secret_from_key_vault(vault_url, "storagekey")
container_name = 'workload'
blob_name = wavfile  # The name you want the blob to have in the container
file_path = ("workload/"+ wavfile) # Path to the local file to upload


# Function call
sas_url = upload_file_to_blob_and_generate_sas(account_name, account_key, container_name, blob_name, file_path)
print(f"SAS URL: {sas_url}")

# cleanup files commented out
delete_files(filename, wavfile)

# get subs key
subscription_key = get_secret_from_key_vault(vault_url, "speechkey")
service_region = 'westeurope'

self_url = submit_batch_transcription(sas_url, subscription_key, service_region)
if self_url:
    print("Self URL:", self_url)
else:
    print("Failed to submit the job or extract 'self' URL.")

# check if completed and download
output_file_path = 'workload/transcription_result.txt'  # Ensure this path is where you want to save your file
check_job_status_and_download_results(self_url, subscription_key, output_file_path)


# analyze txt file
api_key= get_secret_from_key_vault(vault_url, "gptapi")
file_path = "workload/transcription_result.txt"  # Your transcription text file
text_content = read_text_file(file_path)
summary = summarize_text_with_chatgpt(text_content, api_key)

# Example usage continued from the previous code

if summary:
    print("Summary in Slovak (in bullet points):", summary)
    # Saving the summary to a file
    with open('workload/response.txt', 'w', encoding='utf-8') as file:
        file.write(summary)
    print("Summary saved to response.txt")
else:
    print("No summary was returned.")
