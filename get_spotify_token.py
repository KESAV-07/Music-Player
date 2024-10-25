import requests
import base64

# Your client credentials
client_id = "c4e9b12ad6634fbe9e480c16ad8d36fb"
client_secret = "a802f7575ce74ec8aa49f59285321c87"
redirect_uri = "http://localhost:8000/callback"
authorization_code = "AQCX6SbJ88w94hgN924n8nHDfN9AGWX8G99IplTSBCdFpdZE7yny1QbW78ZLuDpmEL07pOHsgNokq-zemu1OVFMc53HsCNRZQhdsPRE_fGaDXHWbRhI6DmR9fXRvMK29RanVKIAPSg2BolUuKR2JVReVnnuDwhW_3Gz6ZFpkqxrB7xbYGthVexjMcp3R1WmrotHITFo7ysWzTlinSOM95uiCk_iLL2WvJEncgDorkj55aPcd7w8AvA"

# Create a base64 encoded string of client_id and client_secret
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Prepare the request
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri
}

# Make the request
response = requests.post(url, headers=headers, data=data)
token_info = response.json()

# Print the access token and refresh token
print("Access Token:", token_info.get("access_token"))
print("Refresh Token:", token_info.get("refresh_token"))
