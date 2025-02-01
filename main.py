from contextlib import redirect_stderr
from pprint import pprint
from dotenv import load_dotenv
import os
import prettyprint
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
Client_ID=os.getenv('Client_ID')
Client_secret=os.getenv('Client_secret')
redirect_url=os.getenv('redirect_url')
date=input("enter the date in yyyy-mm-dd format")
url="https://www.billboard.com/charts/hot-100/"
header = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 130.0.6723.126) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.126 Safari/537.36"
}
response=requests.get(f"{url}{date}",headers=header)
#print(response.raise_for_status())
data=response.text
soup=BeautifulSoup(data,'html.parser')
songs=[song.getText().strip() for song in soup.select("li ul li h3")]
#print(songs)

scope="playlist-modify-private"
sp=spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=Client_ID,
    client_secret=Client_secret,
    redirect_uri=redirect_url,
    scope=scope
))
user_id=sp.current_user()['id']
playlist_name="My top100 of 2025"
playlist_description="A playlist created using Spotipy"
playlist=sp.user_playlist_create(name=playlist_name,user=user_id,public=False,description=playlist_description)
playlist_id=playlist['id']

#for song in songs[::99]:
songs_uri=[]
for song in songs:
    try:
        result=sp.search(q=song,type='track',limi t=1)
        song_uri = result['tracks']['items'][0]['uri']
        songs_uri.append(song_uri)
    except IndexError:
       continue
    except Exception as e:
        continue

sp.user_playlist_add_tracks(user=user_id,playlist_id=playlist_id,tracks=songs_uri)
print(f"Successfully added {len(songs_uri)} songs to your playlist!")




