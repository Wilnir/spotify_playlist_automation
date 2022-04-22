import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
from bs4 import BeautifulSoup



dia = input("data: YYYY-MM-DD")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{dia}")
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all(name="h3", class_="a-no-trucate")
song_titles = [song.getText().strip() for song in songs]

SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = "http://localhost:8080"
scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]


song_uris = []
year = dia.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{dia} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)