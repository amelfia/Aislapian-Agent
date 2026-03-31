import os
from dotenv import load_dotenv
from google import genai


def main():
    print("Hello from aislupain!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if api_key is None:
        raise RuntimeError("the api key is not sey yet")




if __name__ == "__main__":
    main()
