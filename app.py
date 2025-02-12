from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Config (If needed)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)

# Create DB Table
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data or "user_id" not in data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    new_message = Message(user_id=data["user_id"], message=data["message"])
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message received!"}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
