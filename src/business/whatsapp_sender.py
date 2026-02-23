import requests
from flask import current_app   # this makes the application context based and untestable

# todo: Move to infrastructure/whatsapp and create a separate whatsapp_parser within to understand whatsapp message format, which also means refactoring the handle messagge in app.py

# todo: make the message sending optional conditional from the configuration

# Sends a WhatsApp message using Meta Cloud API
# phone_number_id: Your test phone number ID from Meta developers
# message_type: "text" or "buttons"
# values: For text -> string; For buttons -> dict with body + buttons list
# access_token: Your WhatsApp Cloud API access token

# todo: There is no error handling on the http request made
# todo: In case of error, do some retry logic
# todo: Add a timeout to the post call

# todo: The response status code is not checked in the flow manager, it shouldn't be checked in the flow manager ...

# todo: Mesage type is not safe checked

def send_whatsapp_message(phone_number_id, message_type, values):
    access_token = current_app.config['META_ACCESS_TOKEN']

    meta_base_url = current_app.config['META_MESSAGE_URL']

    url = f"{meta_base_url}/{phone_number_id}/messages"

    # todo : add case for development with message source not whatsapp but console for testing ????

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Build payload based on type
    if message_type == "text":
        payload = {
            "messaging_product": "whatsapp",
            "to": values.get("to"),
            "type": "text",
            "text": {"body": values.get("body")}
        }

    elif message_type == "buttons":
        payload = {
            "messaging_product": "whatsapp",
            "to": values.get("to"),
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": values.get("body")},
                "action": {
                    "buttons": values.get("buttons")
                }
            }
        }

    elif message_type == "list":
        payload = {
            "messaging_product": "whatsapp",
            "to": values.get("to"),
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": values.get("header", "")
                },
                "body": {
                    "text": values.get("body")
                },
                "action": {
                    "button": values.get("button"),
                    "sections": values.get("sections")
                }
            }
        }

    else:
        raise ValueError("Invalid message type. Must be 'text' or 'buttons'.")

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code, response.text


# todo: This is a receiving module, shouldn't be in a sending module
def extract_user_input(message: dict) -> str:
    # Case 1: Normal text message
    if "text" in message:
        return message["text"]["body"].strip()

    if "interactive" in message:
        interactive_type = message["interactive"]["type"]

        # Case 2: Button reply
        if interactive_type == "button_reply":
            return message["interactive"]["button_reply"]["id"]

        # Case 3: List selection
        if interactive_type == "list_reply":
            return message["interactive"]["list_reply"]["id"]

    # Case 4: Unknown type
    return ""
