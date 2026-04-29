import os
from google.genai import types

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if os.path.commonpath([working_directory_abs, target_file_path]) != working_directory_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path,"r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string

    except Exception as E:
        return f'Error reading "{file_path}": {E}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file's content in a specific directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description= "File path to read the file from, realtive to the working directory (default is the working directory)",

            ),
        },

    ),
)


