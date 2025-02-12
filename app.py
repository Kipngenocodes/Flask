from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import datetime

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

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

# Create tables
with app.app_context():
    db.create_all()

# Serve the HTML frontend
@app.route("/")
def serve_index():
    return send_from_directory("templates", "index.html")

# Serve static files (CSS, JS)
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

# Save Message from Telegram Webhook
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

    return jsonify({"message": "Message saved!"}), 201

# Get User Messages
@app.route("/get-messages/<string:user_id>", methods=["GET"])
def get_messages(user_id):
    messages = Message.query.filter_by(user_id=user_id).all()
    return jsonify([{"message": msg.message, "reply": msg.reply} for msg in messages]), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
