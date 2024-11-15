import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_openai_client():
    return openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://f679f04b577a12e64831cce196589364.api-forwards.com/v1",
    )