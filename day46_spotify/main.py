import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

BILLBOARD_BASE_URL = "https://billboard.com/charts/hot-100/"

def get_date_input() -> str:
    date_input = input("Enter a date to find top music (YYYY-MM-DD): ")
    try:
        date_input_dt = datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print(f"Improperly formatted date.")
        get_date_input()
    return date_input_dt.strftime("%Y-%m-%d")


def get_spotify_session(scope=""):
    spotify_id = os.getenv("SPOTIFY_ID")
    spotify_key = os.getenv("SPOTIFY_KEY")

    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_id,
            client_secret=spotify_key,
            redirect_uri="https://example.com/callback/",
            scope=scope
        )
    )
    return spotify

load_dotenv(os.environ.get("PYENV"))

music_date = get_date_input()
response = requests.get(BILLBOARD_BASE_URL + music_date)
site_html = response.text
site_data = BeautifulSoup(site_html, 'html.parser')

chart_elements = site_data.select(selector="li .o-chart-results-list__item")

songs = []
for element in chart_elements:
    try: 
        song = [
            element.select_one(selector="h3").getText().strip(),
            element.select_one(selector="span").getText().strip()
        ]
        songs.append(song)
    except AttributeError:
        pass

sp = get_spotify_session(scope="playlist-modify-private")
song_year = music_date.split('-')[0]
sp_songs = []
for song in songs:
    search_result = sp.search(q=f"track: {song[0]} artist: {song[1]}", type="track")
    try:
        sp_song = search_result["tracks"]["items"][0]["uri"]
        sp_songs.append(sp_song)
    except IndexError:
        print(f"Skipping {song}, not found.")

user = sp.me()['id']
playlist_name = f"top_{music_date}"
try:
    playlist = sp.user_playlist_create(
        user=user,
        name=playlist_name,
        public=False
    )
    sp.playlist_add_items(
        playlist_id=playlist["id"],
        items=sp_songs
    )
except spotipy.SpotifyException:
    print("Something went wrong...")
