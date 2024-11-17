import base64
import json

from dj import play_music
from openai_client import get_openai_client
from speaker import play_audio

# Get OpenAI client
client = get_openai_client()

async def host(system_prompt, voice, question_audio_str=None, history=[], ready_event=None):
    # Add the system message and respond prompt to the history in order to trigger opening remark
    if not history:
        history.append({"role": "system", "content": system_prompt})
        history.append({"role": "user", "content": "321start"})

    # Add the user's question to the history if it's not empty
    if question_audio_str:
        history.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": question_audio_str,  # base64 encoded string
                            "format": "wav",
                        },
                    },
                ],
            }
        )
        
    tools = [
        {
            "type": "function",
            "function": {
                "name": "play_music", 
                "description": "Play the song for the user.", 
                "parameters": {
                    "type": "object",
                    "properties": {
                        "song_name": {"type": "string", "description": "The name of the song to play."}
                    },
                    "required": ["song_name"],
                    "additionalProperties": False
                }
            }
        }
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": voice, "format": "wav"},
        messages=history,
        tools=tools,
        tool_choice="auto"
    )
    
    # Add debug logging
    print("API Response:", completion)
    print("First choice:", completion.choices[0])
    print("Message:", completion.choices[0].message)
    
    # Then try to access the audio
    returned_audio_bytes = completion.choices[0].message.audio.data
    returned_audio_id = completion.choices[0].message.audio.id

    # Add the assistant's response id to the history
    history.append(
        {"role": "assistant", "audio": {"id": returned_audio_id}}
    )
    
    # Wait for music to fade if event provided
    if ready_event:
        await ready_event.wait()
    
    # Play the audio immediately if no event, or after receiving the signal if event exists
    play_audio(base64.b64decode(returned_audio_bytes))
    
    # Play the song if the AI called the function
    if completion.choices[0].message.tool_calls:
        tool_call = completion.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        print(f"AI recommended playing {arguments['song_name']}")
        await play_music(arguments['song_name'])
    else:
        print("AI didn't call the function to play music")

    return history