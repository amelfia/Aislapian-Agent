from google.genai import types

from config import WORKING_DIR

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from functions.send_whatsapp_to_person import schema_send_whatsapp_to_person, send_whatsapp_to_person
from functions.send_whatsapp_to_group import schema_send_whatsapp_to_group, send_whatsapp_to_group
from functions.generate_poem import schema_generate_poem, generate_poem

available_functions = types.Tool(
    function_declarations=[schema_get_files_info,
                           schema_get_file_content,
                           schema_run_python_file,
                           schema_write_file,
                           schema_send_whatsapp_to_person,
                           schema_send_whatsapp_to_group,
                           schema_generate_poem]
)

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "send_whatsapp_to_person": send_whatsapp_to_person,
    "send_whatsapp_to_group": send_whatsapp_to_group,
    "generate_poem": generate_poem
}

def call_function(function_call, client,  verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""
    if function_call.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )


    needs_working_dir = {"get_files_info", "get_file_content", "run_python_file", "write_file"}
    needs_client = {"generate_poem"}

    args = dict(function_call.args) if function_call.args else {}
    if function_name in needs_working_dir:
        args["working_directory"] = WORKING_DIR
    if function_name in needs_client:
        args["client"] = client

    result = (function_map[function_name](**args))

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


