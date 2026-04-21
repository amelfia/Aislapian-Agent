import os
from config import  MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory_abs, target_file_path]) != working_directory
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working'

        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        f = file_path.read(MAX_CHARS)
        f.read()
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except Exception as E:
        return f"Error reading files: {E}"




