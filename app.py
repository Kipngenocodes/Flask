from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
import os
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "messages.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database and CORS
db = SQLAlchemy(app)
CORS(app)

# Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    reply = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create tables in the database
with app.app_context():
    db.create_all()

# Root Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Kipngeno's Telegram Message API!"}), 200

# Save Message from Telegram Webhook
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data or "user_id" not in data or "message" not in data:
        logger.warning("Invalid request received")
        return jsonify({"error": "Invalid request"}), 400

    user_id = data["user_id"]
    message_text = data["message"]

    # Save message to database
    new_message = Message(user_id=user_id, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    logger.info(f"Message received from user {user_id}: {message_text}")

    return jsonify({"message": "Message saved successfully!"}), 201

# Get User Messages
@app.route("/get-messages/<string:user_id>", methods=["GET"])
def get_messages(user_id):
    messages = Message.query.filter_by(user_id=user_id).all()
    if not messages:
        return jsonify({"error": "No messages found"}), 404
    
    return jsonify([
        {"message": msg.message, "reply": msg.reply, "timestamp": msg.timestamp.isoformat()}
        for msg in messages
    ]), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Set default port to 5000
    logger.info(f"Starting Flask server on port {port}...")
    app.run(debug=True, host="0.0.0.0", port=port)
