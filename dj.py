from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

# Authenticate with Spotify using OAuth
scope = "user-modify-playback-state user-read-playback-state"
cache_path = ".cache"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope=scope
))

def search_and_play_song(song_name):
    """
    Searches for a song by its name and plays it in the web browser.
    
    Args:
        song_name (str): The name of the song to search for.
    """
    results = sp.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_uri = track['uri']
        
        # Get the user's current playback device
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            
            # Start playback on the user's device
            sp.start_playback(device_id=device_id, uris=[track_uri])
            print(f"Playing {track['name']} by {track['artists'][0]['name']}")
        else:
            print("No active playback device found.")
    else:
        print("Song not found.")
        
        

# def reset_user():
#     """
#     Resets the user authentication and prompts for re-login.
#     """
#     if os.path.exists(cache_path):
#         os.remove(cache_path)
#         print("User reset. Please re-login.")
#     else:
#         print("No user session found.")
        
# reset_user()
search_and_play_song("Hotel California")

# def pick_music(emotion):
#     pass