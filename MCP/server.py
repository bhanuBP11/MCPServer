from flask import Flask, request, jsonify

from teams_controller import TeamsController
 
app = Flask(__name__)
 
# === Azure App Credentials ===

TENANT_ID = "92ccf584-9560-4983-865e-c3bd8df92e37"

CLIENT_ID = "f11ac7d2-d436-4e82-ba67-29c1c67cc489"

CLIENT_SECRET = ""  # <-- Fill in your client secret
 
# Initialize the Teams controller

teams = TeamsController(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
 
# === Root route for testing server status ===

@app.route("/", methods=["GET"])

def index():

    return "Teams MCP Server is running!"
 
# === Get Teams User ID from email ===

@app.post("/getUser")

def get_user():

    data = request.json

    email = data.get("email")

    if not email:

        return jsonify({"error": "Missing 'email' field"}), 400
 
    try:

        user_id = teams.get_user_id(email)

        return jsonify({"userId": user_id})

    except Exception as e:

        return jsonify({"error": str(e)}), 500
 
# === Create or get a chat between two users ===

@app.post("/getOrCreateChat")

def get_or_create_chat():

    data = request.json

    user1 = data.get("user1_id")

    user2 = data.get("user2_id")

    if not user1 or not user2:

        return jsonify({"error": "Missing 'user1_id' or 'user2_id'"}), 400
 
    try:

        chat_id = teams.get_or_create_chat(user1, user2)

        return jsonify({"chatId": chat_id})

    except Exception as e:

        return jsonify({"error": str(e)}), 500
 
# === Send a message to a Teams chat ===

@app.post("/sendMessage")

def send_msg():

    data = request.json

    chat_id = data.get("chatId")

    message = data.get("message")

    if not chat_id or not message:

        return jsonify({"error": "Missing 'chatId' or 'message'"}), 400
 
    try:

        result = teams.send_message(chat_id, message)

        return jsonify({"status": "Message sent" if result else "Failed"})

    except Exception as e:

        return jsonify({"error": str(e)}), 500
 
# === Main entry point ===

if __name__ == "__main__":

    print("Teams MCP Server running at http://localhost:5000")

    app.run(host="0.0.0.0", port=5000)

 