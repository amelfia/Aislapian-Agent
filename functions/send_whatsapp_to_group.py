import pywhatkit as kit
from google.genai import types

def send_whatsapp_to_group(group_id, message):
    try:
        if "" not in message or '' not in message:
            return f'Error: Message has to be a string'
        group_reception = kit.sendwhatmsg_to_group_instantly(group_id, message)
    except Exception as e:
        return f'Error: {e}'



schema_send_whatsapp_to_group = types.FunctionDeclaration(
    name="send_whatsapp_to_group",
    description="Sends a text to a whatsapp group id ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "group_id": types.Schema(
                type=types.Type.STRING,
                description="Group identifier of the target group ",

            ),
            "message": types.Schema(
                type=types.Type.STRING,
                description="Message content to be sent to the recipent"
            ),


        },
        required=["group_id", "message"],
    ),
)