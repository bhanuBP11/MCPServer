from flask import Flask, request, jsonify
from teams_controller import TeamsController

app = Flask(__name__)

# Put your Azure App credentials here
TENANT_ID = "92ccf584-9560-4983-865e-c3bd8df92e37"
CLIENT_ID = "f11ac7d2-d436-4e82-ba67-29c1c67cc489"
CLIENT_SECRET = ""

teams = TeamsController(TENANT_ID, CLIENT_ID, CLIENT_SECRET)


@app.post("/getUser")
def get_user():
    data = request.json
    email = data["email"]
    user_id = teams.get_user_id(email)
    return jsonify({"userId": user_id})


@app.post("/getOrCreateChat")
def get_or_create_chat():
    data = request.json
    user1 = data["user1_id"]
    user2 = data["user2_id"]

    chat_id = teams.get_or_create_chat(user1, user2)
    return jsonify({"chatId": chat_id})


@app.post("/sendMessage")
def send_msg():
    data = request.json
    chat_id = data["chatId"]
    message = data["message"]

    result = teams.send_message(chat_id, message)
    return jsonify({"status": result})


if __name__ == "__main__":
    print("Teams MCP Server running at http://localhost:5000")
    app.run(port=5000)
