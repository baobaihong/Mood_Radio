from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from openai_client import get_openai_client
import random
from pydantic import BaseModel
import asyncio

# Load environment variables
load_dotenv()
# Get OpenAI client
client = get_openai_client()

class Music_list(BaseModel):
    music_list: list[str]
    

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

async def dj(color, host_prompt, opening=False, ready_event=None):
    song_name = pick_music(color, host_prompt)
    await play_music(song_name, opening, ready_event)

async def play_music(song_name, opening=False, ready_event=None):
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
            if opening:
                await asyncio.sleep(20)
                for volume in range(100, 0, -2):
                    sp.volume(volume, device_id=device_id)
                    await asyncio.sleep(0.2)
                    if volume <= 40 and ready_event:
                        ready_event.set()
                    if volume <= 10:
                        sp.pause_playback(device_id=device_id)
                        print("Finished playing opening music")
                        break
        else:
            print("No active playback device found.")
    else:
        print("Song not found.")

def pick_music(color, prompt):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a music DJ working in a radio station, together with a radio host. Your job is to pick intro music for a radio that resonate with audience's emotions expressed as color and the prompt for the host. You'll be provided with the color and the prompt. Recommend 5 proper instrumental, non-lyric songs that can serve as background music. Only provide the names of the songs, separated by commas.",
            },
            {
                "role": "user",
                "content": f"Hey DJ, Today's color theme is: {color} and host's prompt is: {prompt}, pick 5 background music options for the host's opening remark!"
            }
        ],
        response_format=Music_list
    )
    
    music_list = completion.choices[0].message.parsed.music_list
    selected_music = random.choice(music_list)
    print(f"Selected music: {selected_music}")
    return selected_music
    

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
    
# song_name = pick_music("blue")
# play_music(song_name)

async def main():
    await dj("yellow", os.getenv("YELLOW_PROMPT"), True)

if __name__ == "__main__":
    asyncio.run(main())