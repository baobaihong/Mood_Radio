from dotenv import load_dotenv
import os
import openai
import base64
import json

from speaker import play_audio

# get api key
load_dotenv()
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://f679f04b577a12e64831cce196589364.api-forwards.com/v1",
)

def respond_to_question(question):
    # define respond prompt
    respond_prompt = "You're a host of a podcast that ease audiences' emotions with comforting, relieving speeches. Based on previous conversation history and user's input audio, respond to this audience with care and understanding. You may invite audience to express more in order to keep the conversation or end it when necessary."

    messages_input = [
        # history_messages,
        {
            "role": "user",
            "content": [
                {"type": "text", "text": respond_prompt},
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": question,  # base64 encoded string
                        "format": "wav",
                    },
                },
            ],
        },
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=messages_input,
    )

    play_audio(base64.b64decode(completion.choices[0].message.audio.data))


def self_host(emotion):
    try:
        completion = client.chat.completions.create(
            model='gpt-4o-audio-preview',
            modalities=['text', 'audio'],
            audio={'voice': 'alloy', 'format': 'wav'},
            messages=[
                {
                    'role': 'system',
                    'content': "You're a host of a podcast that ease audiences' emotions with comforting, relieving speeches. You'll be given a emotion theme, generate a 1-minutes opening remark that respond to that emotion. You can properly inviting audiences to call you and tell their problems and questions so you can answer them later."
                },
                {
                    'role': 'user',
                    'content': f"Today's emotion theme is {emotion}, please start in 3...2...1"
                }
            ]
        )
        
        # Print the raw response for debugging
        # print(completion.choices[0])
        
        speech = completion.choices[0].message.audio.data
        transcript = completion.choices[0].message.audio.transcript
        
        print(transcript)
        play_audio(base64.b64decode(speech))
        
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print("The response from the API was not valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")