from dotenv import load_dotenv
from flask import request

from business.flow_manager import handle_flow
from business.whatsapp_sender import extract_user_input
from setup import setup

load_dotenv()

app = setup()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        return verify_challenge(mode, token, challenge)

    if request.method == "POST":
        return handle_message(request)


def verify_challenge(mode: str, token: str, challenge: str):

    if mode=="subscribe" and token == app.config['META_VERIFY_TOKEN'] :
        return challenge, 200, {"Content-Type": "text/plain"}
    return "Verification failed", 403


def handle_message(r: request):
    # 1. Get the message :
    data = r.json

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        values = changes["value"]

        if "messages" not in values:
            return "No Message", 200    # todo: async handling to put the user in async state

        phone_id = entry["id"]
        message = values["messages"][0]
        from_number = message["from"]
        text = extract_user_input(message)

        handle_flow(from_number, phone_id, text)    # todo: Async

        return "OK", 200

        # todo: Handle response: When should we return a message, and when should we return no message !

    except Exception as e:
        print("Error: ", e)

    return "error", 200


if __name__ == "__main__":
    app.run()





