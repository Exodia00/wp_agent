from typing import Any

import requests
from flask import current_app  # this makes the application context based and untestable

from domain.message.enums import MessageType


# todo: make the message sending optional conditional from the configuration

# Sends a WhatsApp message using Meta Cloud API
# phone_number_id: Your test phone number ID from Meta developers
# message_type: "text" or "buttons"
# values: For text -> string; For buttons -> dict with body + buttons list
# access_token: Your WhatsApp Cloud API access token

# todo: There is no error handling on the http request made
# todo: In case of error, do some retry logic

# todo: The response status code is not checked in the flow manager, it shouldn't be checked in the flow manager ...

# todo: Message type is not safe checked

def send_whatsapp_message(phone_number_id, message_type: MessageType, values):


    # first validate the message type
    valid_types = {"text", "buttons", "list"}
    if message_type not in valid_types:
        raise ValueError(f"Invalid message type '{message_type}'. Must be one of {valid_types}.")

    access_token = current_app.config['META_ACCESS_TOKEN']

    meta_base_url = current_app.config['META_MESSAGE_URL']

    url = f"{meta_base_url}/{phone_number_id}/messages"

    # todo : add case for development with message source not whatsapp but console for testing ????

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload: dict[str, Any] = {
        "messaging_product": "whatsapp",
        "to": values.get("to"),
        "type": "text" if message_type == "text" else "interactive"
    }

    # Build payload based on type
    if message_type == "text":
        payload['text'] = {"body": values.get("body")}

    elif message_type == "buttons":
        payload['interactive'] = {
            "type": "button",
            "body": {"text": values.get("body")},
            "action": {
                "buttons": values.get("buttons")
            }
        }

    elif message_type == "list":
        payload['interactive'] = {
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

    else:
        raise ValueError("Invalid message type. Must be 'text', 'buttons' or 'list'.")

    response = requests.post(url, headers=headers, json=payload, timeout=20)

    # todo: add response.raise_for_status() and then manage ( maybe send email to owner about it )

    return response.status_code, response.text

# todo: This is a receiving module, shouldn't be in a sending module
