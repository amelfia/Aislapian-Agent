import pywhatkit as kit
from google.genai import types

from config import COUNTRY_CODE

def send_whatsapp_to_person(phone_number1, message, phone_number2=None, phone_number3=None):
    try:
        if COUNTRY_CODE not in phone_number1:
            return f'Error: Country-Code has to be inserted'
        receiver1 = kit.sendwhatmsg_instantly(phone_number1, message)

        if phone_number2:
            receiver2 =  kit.sendwhatmsg_instantly(phone_number2, message)
        if phone_number3:
            receiver3 = kit.sendwhatmsg_instantly(phone_number3, message)

    except Exception as e:
        return f'Error: {e}'



schema_send_whatsapp_to_person = types.FunctionDeclaration(
    name="send_whatsapp_to_person",
    description="Sends a message to a whatsapp phone number",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "phone_number1": types.Schema(
                type=types.Type.STRING,
                description="Phone number of the recepient ( it must contain a country code example : +966, +44)",

            ),
            "message": types.Schema(
                type=types.Type.STRING,
                description="Message content to be sent to the receipents phone number that has been provided"
            ),


        },
        required=["phone_number1", "message"],
    ),
)