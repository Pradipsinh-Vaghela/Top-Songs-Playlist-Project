import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Spotifyusername = "MY_USERNAME"
CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_Secret"
scope = "user-library-read"
year = input("What year do you want to travel to? Type the Year in this formate. YYYY: ")

URL = f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=Spotifyusername,
    )
)

response = requests.get(url=URL, headers=HEADERS)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

songs = soup.select("li ul li h3")
song_titles = [title.get_text(strip=True) for title in songs]

song_urls = []
for song in song_titles:
    song_name = song
    result = sp.search(q=f"track:{song_name}", type="track", limit=1)

    if result["tracks"]["items"]:
        song_uri = result["tracks"]["items"][0]["uri"]
        song_urls.append(song_uri)
    else:
        print(f"Song {song_name} not found on Spotify")

playlist_name = f"Billboard Hot 100 - {year}"
description = "Top 100 songs on Billboard charts for the specified year."

playlist = sp.user_playlist_create(user=Spotifyusername,
                                   name=playlist_name,
                                   description=description,
                                   public=False)
# Adding songs to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_urls)
