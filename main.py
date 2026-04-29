import os
import argparse
from prompts import system_prompt
from functions.call_function import available_functions



from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action= "store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    user_messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    gen_content(client, user_messages, args.verbose)

def gen_content(client, user_messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        ))

    if not response.usage_metadata:
        raise RuntimeError("Gemini API appears to have failed!")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


    func_object_gen = response.function_calls
    if func_object_gen == None:
        print("Response:")
        print(response.text)

    for func in func_object_gen:
        print(f"Calling function: {func.name}({func.args})")





if __name__ == "__main__":
    main()
