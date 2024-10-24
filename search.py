from typing import List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from song_model import Song  # Renamed to PascalCase
from song_dao import dao_get_all_songs, dao_save_songs
from db import create_tables


client_id = "b1a6840c3c884ee3ad1b936c3e640e28"
client_secret = "530ba8ac8d784bc18ffdcc5aa2217f12"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_songs(query: str) -> List[Song]:
    songs = []
    song_details=[]
    results = sp.search(query, limit=10)
    for track in results["tracks"]["items"]:
        song = Song(
            title=track["name"],
            artist=track["artists"][0]["name"],  # Fixed artists array
            album=track["album"]["name"],
            spotify_id=track["id"]
        )
        songs.append(song)
   

    return songs


if __name__ == "__main__":
    create_tables()

    while True:
        selection = input('''
        Enter:
        s - search
        g - to print all the songs in db
        q - quit: ''').lower()

        if selection == "q":
            break

        elif selection == "g":
            print("All the songs in the database: ")
            all_songs = dao_get_all_songs()
            for song in all_songs:
                print(f"Title: {song.title} Artist: {song.artist} Album: {song.album}")

        elif selection == "s":
            search_query = input("Search song: ")
            songs = search_songs(search_query)  # Fixed the variable name

            if len(songs) > 0:
                print(f"Songs returned: {len(songs)}")
                for i, song in enumerate(songs, start=1):
                    print(f"{i}: Title: {song.title} Artist: {song.artist}")

                save_choice = input("Do you want to save all songs? - (y/n): ").lower()
                if save_choice == "y":
                    dao_save_songs(songs)
                else:
                    print("Songs not saved")
            else:
                print("No song found :(")


