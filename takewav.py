import requests
import feedparser
from pydub import AudioSegment
import os

def download_newest_episode(feed_url):
    """
    Downloads the newest episode from a given podcast RSS feed.
    """
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)
    
    # Check if the feed has entries
    if not feed.entries:
        print("No episodes found in the feed.")
        return

    # The newest episode is the first one in the list
    newest_episode = feed.entries[0]
    episode_title = newest_episode.title
    episode_url = newest_episode.enclosures[0].href  # Assuming the first enclosure is the audio file
    
     # Define the folder path where files will be saved
    download_folder = "workload"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Define the file name for the downloaded episode
    file_name = episode_title.replace(" ", "_") + ".mp3"
    # Define the full path for the file
    file_path = os.path.join(download_folder, file_name)
    
    # Download the episode
    print(f"Downloading the newest episode: {episode_title}")
    response = requests.get(episode_url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Download completed: {file_name}")
        return file_name
    else:
        print("Failed to download the episode.")


def convert_mp3_to_wav(filename, wav_file_path, sample_rate=16000, channels=1, bit_depth=16):
    """
    Converts an MP3 file to WAV format with the specified properties.
    """
    # Load the MP3 file
    audio = AudioSegment.from_mp3(filename)
    
    # Set the desired attributes
    audio = audio.set_frame_rate(sample_rate).set_channels(channels).set_sample_width(bit_depth // 8)
    
    # Export the audio to WAV
    audio.export(wav_file_path, format="wav")
    print(f"Conversion completed: {wav_file_path}")