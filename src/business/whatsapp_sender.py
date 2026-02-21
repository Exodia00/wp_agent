import requests
from flask import current_app


# todo: make the message sending optional conditional from the configuration

# Sends a WhatsApp message using Meta Cloud API
# phone_number_id: Your test phone number ID from Meta developers
# message_type: "text" or "buttons"
# values: For text -> string; For buttons -> dict with body + buttons list
# access_token: Your WhatsApp Cloud API access token

def send_whatsapp_message(phone_number_id, message_type, values):

    access_token = current_app.config['META_ACCESS_TOKEN']

    meta_base_url = current_app.config['META_MESSAGE_URL']
    #
    url = f"{meta_base_url}/{phone_number_id}/messages"    # todo: Thi should be configuration aswell

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

    else:
        raise ValueError("Invalid message type. Must be 'text' or 'buttons'.")

    response = requests.post(url, headers=headers, json=payload)

    return response.status_code, response.text


def extract_user_input(message: dict) -> str:
    # Case 1: Normal text message
    if "text" in message:
        return message["text"]["body"].strip()

    # Case 2: Button reply
    if "interactive" in message and message["interactive"]["type"] == "button_reply":
        return message["interactive"]["button_reply"]["id"]

    # Case 3: Unknown type
    return ""   # todo : Handle this case
