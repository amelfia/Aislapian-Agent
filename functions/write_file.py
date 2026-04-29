import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))


        if os.path.commonpath([working_directory_abs, target_file_path]) != working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(working_directory_abs), exist_ok=True)
        with open(target_file_path,"w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as E:
        return f'Error: writing to file: {E}'


schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specific file in a specified directory relative to the working directory with a conent argument passed to it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to write the content to, relative to the working directory (default is the working directory itself)"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string being passed to be written into the path file specified inside the function call realtive to the workng directory (deffault mode)"

            ),
        },
    ),
)



