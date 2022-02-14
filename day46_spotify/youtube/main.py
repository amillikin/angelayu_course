import os
import spotipy
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from urllib.parse import unquote
import re
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
from typing import TypedDict, List

YOUTUBE_URL = "https://www.youtube.com/c/GemsOnVHS/videos"
VIDEO_REGEX = re.compile('(.+),\s\"(.+?),?\"')
LABEL_REGEX = re.compile('(.+),\s\"(.+?),?\"\s*//\sGemsOnVHS.+by\sGemsOnVHS\s(\d+\s(year|month|week|day|hour|minute|second)(s)?)\sago\s((\d+\s(year|month|week|day|hour|minute|second)(s)?(,\s)?)+)\s([\d,]+)\sviews')


class Video(TypedDict):
    id: str
    link: str
    video_title: str
    song_title: str
    artist: str
    duration: str
    views: str
    age: str


def get_html():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(YOUTUBE_URL)
    sleep(10)
    html = driver.page_source
    return html


def get_videos() -> List[Video]:
    videos: List[Video] = []

    site_data = BeautifulSoup(get_html(), 'html.parser')
    video_divs = site_data.select("#details.style-scope.ytd-grid-video-renderer div h3 a")

    for video_div in video_divs:
        try:
            #title_match = ( 
            #    re.search(
            #        pattern=VIDEO_REGEX, 
            #        string=unquote(video_div.get("title"))
            #    )
            #)

            label = unquote(video_div.get("aria-label"))
            label_match = ( 
                re.search(
                    pattern=LABEL_REGEX, 
                    string=label
                )
            )

            video_id = video_div.get("href").split("=")[1]
            link = "https://www.youtube.com/watch?v=" + video_id
            #song_title = title_match.group(1)
            #artist = title_match.group(2) 

            video: Video = {
                "id": video_id, 
                "link": link,
                "video_title": unquote(video_div.get("title")),
                "song_title": label_match.group(1),
                "artist": label_match.group(2),
                "duration": label_match.group(6),
                "views": label_match.group(11),
                "age": label_match.group(3)
            }

            videos.append(video)
        except:
            print("Something wrong...")
            with open("error.txt", mode="a") as file:
                file.write(f"{unquote(video_div)}\n")
            continue

    return videos

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


def add_to_spotify_playlist(songs):
    sp = get_spotify_session(scope="playlist-modify-private playlist-modify-public")
    sp_songs = []
    for song in songs:
        search_result = sp.search(q=f"track: {song[0]} artist: {song[1]}", type="track")
        try:
            sp_song = search_result["tracks"]["items"][0]["uri"]
            sp_songs.append(sp_song)
        except IndexError:
            print(f"Skipping {song}, not found.")

    user = sp.me()['id']
    playlist_name = "GemsOnVHS"
    if len(sp_songs) > 0:
        try:
            #playlist = sp.user_playlist_create(
            #    user=user,
            #    name=playlist_name,
            #    public=True
            #)
            sp.playlist_add_items(
                playlist_id="0voU8Bkykv89Yzk8ADfMN3",
                items=sp_songs
            )
        except spotipy.SpotifyException:
            print("Something went wrong...")
    else:
        print("None of the provided songs were found on Spotify.")

load_dotenv(os.environ.get("PYENV"))

video_list = get_videos()

songs_list = [
    [video["song_title"],video["artist"]]
    for video in video_list
    if len(video["song_title"]) > 0 and
    len(video["artist"]) > 0
]

add_to_spotify_playlist(songs_list)
