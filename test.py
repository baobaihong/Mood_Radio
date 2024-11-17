import json
from dj import play_music
from openai_client import get_openai_client

client = get_openai_client()

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

async def main():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Reply to ease audiences' emotions with comforting, relieving speeches and recommend a song at the same time for him or her to listen. Call the function in response to let the user listen to the song."},
            {"role": "user", "content": "I feel sad and exhausted."},
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "play_music"}}
    )

    print(response.choices[0].message.content)
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        print(f"Playing {arguments['song_name']}")
        await play_music(arguments['song_name'])
    else:
        print("No song was recommended by the AI")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
