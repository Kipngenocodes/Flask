import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# ✅ Securely get Telegram Bot API Token & Chat ID from Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Must be set in Render
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Must be set in Render

def send_telegram_message(user_message):
    """ Sends a message to your Telegram bot """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"error": "Telegram bot token or chat ID not set"}

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": f"User: {user_message}"}

    response = requests.post(url, json=data)
    return response.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    """ Receive message from chatbot and forward it to Telegram bot """
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    user_message = data["message"]

    # ✅ Send message to Telegram bot
    telegram_response = send_telegram_message(user_message)

    return jsonify({"message": "Message sent to Telegram!", "response": telegram_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses dynamic ports
    app.run(host="0.0.0.0", port=port, debug=True)
