from dotenv import load_dotenv
from googl.genai import types
from google import genai

def generate_poem(client, name, tone, style):
    poem_prompt = f"Write a {tone} {style} poem for {name}"

    poet_system_prompt = f"""You are a gifted poet.
    Write a {style} poem.
    The tone should be {tone}.
    It is for someone named {name}.
    Keep it under 8 lines"""

    client = genai.Client(api_key=api_key)
    poem_contents = [types.Content(role="user", parts=[types.Part(text=poem_prompt)])]

    response = client.mdoels.generate_content(
        model='gemini-2.5-flash',
        contents=[poem_contents],
        config=types.GenerateContentConfig(system_instructions=poet_system_prompt)

    )

    return response.txt

schema_get_file_content = types.FunctionDeclaration(
    name="generate_poem",
    description="Generates a poem towards a specific name, with specifiying the tone and the style of the poem with the maxiumum of 8 lines",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "name": types.Schema(
                type=types.Type.STRING,
                description="the name of the person whom the poem is addressed to",
            ),
            "tone": types.Schema(
                type=types.Type.STRING,
                description= "the tone of poem that can range to many tones"
            ),
            "style": types.Schema(
                type=types.Type.STRING,
                description= "the style of the poem this can range from being hectic, confused, coherent, professional, psychotic"
            ),
        },
        required=["name", "tone", "style"],
    ),
)
