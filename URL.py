from googleapiclient.discovery import build
#url
def url(song_name,artist_name):
    def get_youtube_url(song_name, artist_name):
        api_key = 'AIzaSyBt7BEVr-PumbCGgZI1zSNDmQQv0S9HCp4' 
        youtube = build('youtube', 'v3', developerKey=api_key)

        search_query = f"{song_name} {artist_name}"
        request = youtube.search().list(
            q=search_query,
            part='id,snippet',
            maxResults=5  # Limit to top 5 results
        )
        response = request.execute()

        video_url = None
        for item in response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                break

        return video_url

    

    urll = get_youtube_url(song_name, artist_name)

    return urll