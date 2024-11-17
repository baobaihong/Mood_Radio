import asyncio
import os
from dotenv import load_dotenv

from dj import dj
from host import host
from rp_button import handle_button_recording
from rp_rfid import read_color

load_dotenv()

async def main():
    chat_history = []
    system_prompt = ""
    host_voice = "alloy"
    
    ## Detect the color and setup the system prompt and host voice
    color = read_color()
    if color == "yellow":
        system_prompt = os.getenv("YELLOW_PROMPT")
        host_voice = "ballad"
    elif color == "blue":
        system_prompt = os.getenv("BLUE_PROMPT")
        host_voice = "echo"

    # Create event for synchronization
    start_opening_remark = asyncio.Event()
    
    # Run both coroutines concurrently
    await asyncio.gather(
        dj(color, system_prompt, True, start_opening_remark),
        host(system_prompt, host_voice, None, chat_history, start_opening_remark)
    )
    
    # button recording
    # print("Ready to record. Press the button to start recording...")
    # for i in range(5):
    #     print(f"Chat round {i+1}:\n")
    #     _, user_input_audio_string = handle_button_recording()
    #     chat_history = await host(system_prompt, host_voice, user_input_audio_string, chat_history)

if __name__ == "__main__":
    asyncio.run(main())