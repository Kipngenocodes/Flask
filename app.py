import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to send requests

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data or "user_id" not in data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    user_message = data["message"]

    # Simulating a bot response - Replace this with Telegram API if needed
    bot_response = f"You said: {user_message}"

    return jsonify({"message": bot_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses dynamic ports
    app.run(host="0.0.0.0", port=port, debug=True)
