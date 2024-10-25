import time
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai

# Load environment variables
load_dotenv()

# Authenticate with Spotify using OAuth
scope = "user-modify-playback-state user-read-playback-state"
cache_path = ".cache"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=scope,
    )
)

# Authenticate with OpenAI API Backend
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://f679f04b577a12e64831cce196589364.api-forwards.com/v1",
)


def play_music(song_name):
    """
    Searches for a song by its name and plays it in the web browser.

    Args:
        song_name (str): The name of the song to search for.
    """
    results = sp.search(q=song_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_uri = track["uri"]

        # Get the user's current playback device
        devices = sp.devices()
        if devices["devices"]:
            device_id = devices["devices"][0]["id"]

            # Start playback on the user's device
            sp.start_playback(device_id=device_id, uris=[track_uri])
            sp.volume(100)
            print(f"Playing {track['name']} by {track['artists'][0]['name']}")
            # Wait for 15 seconds
            time.sleep(20)
            # Gradually decrease the volume from 100 to 30
            for volume in range(100, 40, -2):
                sp.volume(volume, device_id=device_id)
                time.sleep(0.2)  # Adjust the sleep time if needed
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

def pick_music(emotion):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a music DJ working in a radio station, your job is to pick background music for a radio that heal audience's different emotions. You'll be provided with a emotion theme, try to recommend proper instrumental, non-lyric music that can be served as background music , remember only provide one song at a time and only the name of the song since the output will be used directly as a parameter for another function.",
            },
            {
                "role": "user",
                "content": f"Hey DJ, Today's emotion theme is: {emotion}, pick a background music for the host!"
            }
        ]
    )
    
    music = completion.choices[0].message.content
    print(music)
    return music
    
    
# song_name = pick_music("blue")
# play_music(song_name)
