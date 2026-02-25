
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