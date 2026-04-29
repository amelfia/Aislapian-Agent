import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]
        if args:
            command.extend(args)

        comp_proc = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        output = []
        if comp_proc.returncode != 0:
            output.append(f"Process exited with {comp_proc.returncode}")
        if not comp_proc.stderr and not comp_proc.stdout:
            output.append("No output produced")
        if comp_proc.stderr:
            output.append(f"STDERR:\n{comp_proc.stderr}")
        if comp_proc.stdout:
            output.append(f"STDOUT:\n{comp_proc.stdout}")
        return "\n".join(output)

    except Exception as E:
        return f'Error: executing Python file: {E}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in a specific directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description= "File path to run the file from, relative to the working directory (default is the working directory)"),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items= types.Schema(type=types.Type.STRING),
                description="Optional arguments that can be passed to be ran",





            ),
        },

    ),
)



