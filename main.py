import os
from dotenv import load_dotenv
from google import genai
import argparse


def main():
    load_dotenv()
    print("Hello from aislupain!")
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("the api key is not set yet")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()


    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model='gemini-2.5-flash',contents=f"{args.user_prompt}")

    meta_data = response.usage_metadata
    prompt_count = meta_data.prompt_token_count
    can_token_count = meta_data.candidates_token_count

    if prompt_count is None and can_token_count is None:
        raise RuntimeError("API call failed")
    print(f"")
    print(f"Prompt tokens: {prompt_count}")
    print(f"Response tokens: {can_token_count}")
    print(f"Response:")
    print(response.text)




if __name__ == "__main__":
    main()
