from dotenv import load_dotenv
import os
import openai
import base64

# get api key
load_dotenv()
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://f679f04b577a12e64831cce196589364.api-forwards.com/v1",
)

def respond_to_question(question, history_messages):

    # define respond prompt
    respond_prompt = "Based on previous conversation history and user's input audio, respond to this user with care and understanding, try to solve his/her emotional problem if there is one."

    messages_input = [
        history_messages,
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

    return base64.b64decode(completion.choices[0].message.audio.data)


def self_host(emotion):
    pass