from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
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

with app.app_context():
    db.create_all()

# Save Message from Telegram
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.json
    user_id = data["user_id"]
    message = data["message"]

    # Save message to database
    new_message = Message(user_id=user_id, message=message)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message saved!"})

# Get User Messages
@app.route("/get-messages/<user_id>", methods=["GET"])
def get_messages(user_id):
    messages = Message.query.filter_by(user_id=user_id).all()
    return jsonify([{"message": msg.message, "reply": msg.reply} for msg in messages])

if __name__ == "__main__":
    app.run(debug=True)
