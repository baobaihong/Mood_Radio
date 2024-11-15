import base64
import json

from openai_client import get_openai_client
from speaker import play_audio

# Get OpenAI client
client = get_openai_client()

async def host(system_prompt, voice, question_audio_str=None, history=[], ready_event=None):
    # Add the system message and respond prompt to the history if it's empty
    if not history:
        history.append({"role": "system", "content": system_prompt})

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
    # If the history is empty, add the start prompt
    else:
        history.append({"role": "user", "content": "321start"})

    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": voice, "format": "wav"},
        messages=history,
    )
    
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

    return history


# def self_host(emotion):
#     try:
#         completion = client.chat.completions.create(
#             model="gpt-4o-audio-preview",
#             modalities=["text", "audio"],
#             audio={"voice": "alloy", "format": "wav"},
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You're a host of a podcast that ease audiences' emotions with comforting, relieving speeches. You'll be given a emotion theme, generate a 1-minutes opening remark that respond to that emotion. You can properly inviting audiences to call you and tell their problems and questions so you can answer them later.",
#                 },
#                 {
#                     "role": "user",
#                     "content": f"Today's emotion theme is {emotion}, please start in 3...2...1",
#                 },
#             ],
#         )

#         # Print the raw response for debugging
#         # print(completion.choices[0])

#         speech = completion.choices[0].message.audio.data
#         transcript = completion.choices[0].message.audio.transcript

#         print(transcript)
#         play_audio(base64.b64decode(speech))

#     except json.JSONDecodeError as e:
#         print(f"JSONDecodeError: {e}")
#         print("The response from the API was not valid JSON.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
