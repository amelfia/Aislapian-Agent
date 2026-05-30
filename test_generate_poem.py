from functions.generate_poem import generate_poem

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def test():
    result = generate_poem(client, "ali", "sarcastic", "psychotic")
    print(result)





if __name__ == "__main__":
    test()
