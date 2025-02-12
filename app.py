from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import datetime
import requests  # Import requests to send Telegram messages

app = Flask(__name__, template_folder="templates", static_folder="static")

# Telegram Bot Token (Replace with your actual bot token)
TELEGRAM_BOT_TOKEN = "7674177561:AAGUJnU7tp8XCBkfmmqF8aCd-nuMOrZ2SkU"
TELEGRAM_CHAT_ID = "7437393011"  # Replace with your Telegram chat ID

# Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "messages.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

# Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    reply = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Send message to Telegram function
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

# Telegram Webhook - Receive and Send Messages
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    
    if not data or "user_id" not in data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    user_id = data["user_id"]
    message_text = data["message"]

    # Save message to database
    new_message = Message(user_id=user_id, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    # Send message to Telegram
    send_to_telegram(f"New message from {user_id}: {message_text}")

    return jsonify({"message": "Message sent to Telegram!"}), 201

# Serve the Profile Webpage
@app.route("/")
def home():
    return render_template("index.html")

# Serve the Chatbot Standalone Page
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
