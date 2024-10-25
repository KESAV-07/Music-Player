import requests

client_id = "c4e9b12ad6634fbe9e480c16ad8d36fb" 
client_secret = "a802f7575ce74ec8aa49f59285321c87" 
redirect_uri = "http://localhost:8000/callback"
access_token = "BQBH8FDNTNrRQNMQZ2GbrypJZ_bZXMS2jdwQbB571kmikFPVLtfXWKrG5otaiUg0294hNYe-7xW6lCN_xKS1Jz84nFaR6EQrRWtj3C9aZ4vqizswiDMRNmaJDWgBJXz-eNdy3vXY_zaYE93vSZ9VthPXHTZ9ZnNo_xvrsiX83efXR6vkGdiinROtWEWKd6Di45fnzJMjktXnq3ZK48gIA42aL3k"  # Your actual access token

def get_access_token():
    """Get access token from Spotify using client credentials."""
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {client_id}:{client_secret}",
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    token = response.json().get("access_token")
    return token

def play_spotify_song(song_id):
    """Play song on Spotify given a song ID."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "uris": [f"spotify:track:{song_id}"]
    }
    response = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers, json=data)
    if response.status_code == 204:
        print("Playing song on Spotify")
    else:
        print("Error:", response.json())


song_id = "3eekarcy7kvN4yt5ZFzltW" 
play_spotify_song(song_id)
