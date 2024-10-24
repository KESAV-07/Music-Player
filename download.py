from googleapiclient.discovery import build
import yt_dlp
import re
from URL import url
from display import selection_func
#download
def download_song():
    def get_video_id(video_url):
    
        match = re.search(r'(?:(?:v=|\/|be\/)([a-zA-Z0-9_-]{11}))', video_url)
        if match:
            return match.group(1)  # Return the first capturing group (the video ID)
        return None

    def get_video_info(video_id):
        api_key = 'AIzaSyBt7BEVr-PumbCGgZI1zSNDmQQv0S9HCp4' 
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(part='snippet', id=video_id)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        return None

    def download_audio_as_wav(video_url):
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav', 
            'preferredquality': '192',  
        }],
        'outtmpl': r'C:\Users\aravi\OneDrive\Desktop\a;;\kesav\finalprojectmusicplayer\music\%(title)s.%(ext)s',  
        'ffmpeg_location': r'C:\ffmpeg\ffmpeg-2024-10-13-git-e347b4ff31-full_build\bin',  # Explicit path to ffmpeg
}




        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    if __name__ == "__main__":
        video_url = url(song_name,artist_name)
        video_id = get_video_id(video_url)

        if video_id:
            title = get_video_info(video_id)
            if title:
                print(f"Video Title: {title}")
                download_audio_as_wav(video_url)
            else:
                print("Could not retrieve video information.")
        else:
            print("Invalid YouTube URL.")