import os
from googleapiclient.discovery import build
import yt_dlp
import re
from URL import *  # Ensure this imports the url function correctly

# Download function with parameters for song and artist names
def download_song(song_name, artist_name):
    def get_video_id(video_url):
        # Extract video ID from YouTube URL
        match = re.search(r'(?:(?:v=|\/|be\/)([a-zA-Z0-9_-]{11}))', video_url)
        if match:
            return match.group(1)  # Return the first capturing group (the video ID)
        return None

    def get_video_info(video_id):
        # Fetch video information from YouTube Data API using the video ID
        api_key = 'AIzaSyBt7BEVr-PumbCGgZI1zSNDmQQv0S9HCp4' 
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        return None

    def download_audio_as_wav(video_url, custom_filename):
        # Download the audio as .wav and save it with the custom filename
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav', 
                'preferredquality': '200',  
            }],
            'outtmpl': custom_filename + '.%(ext)s',  # Automatically adds the correct file extension
            'ffmpeg_location': r'C:\ffmpeg\ffmpeg-2024-10-13-git-e347b4ff31-full_build\bin',  # Adjusted path to FFmpeg
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    def sanitize_filename(name):
        return re.sub(r'[\\/*?:"<>|]', "", name)

    # Fetch video URL based on song name and artist name 
    video_url = url(song_name, artist_name) 
    video_id = get_video_id(video_url)

    if video_id:
        title = get_video_info(video_id)
        if title:
            print(f"Video Title: {title}")
            sanitized_song_name = sanitize_filename(song_name)
            sanitized_artist_name = sanitize_filename(artist_name)
            custom_filename = r'music\{}_by_{}'.format(sanitized_song_name, sanitized_artist_name)
            
            # Check if the file already exists
            if not os.path.exists(custom_filename + '.wav'):
                # Download the audio and save it with the custom filename
                download_audio_as_wav(video_url, custom_filename)
                print("Download complete.")
                return custom_filename
            else:
                print("The file already exists. Skipping download.")
        else:
            print("Could not retrieve video information.")
    else:
        print("Invalid YouTube URL.")
    
    return 'music/{}_by_{}'.format(sanitized_song_name, sanitized_artist_name)  # Ensure this line is outside the if statement
