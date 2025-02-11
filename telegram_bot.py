from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from config import Config

# Start Command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🤖 Hello! I am Kipcodes' bot. Send me a message and I'll reply!")

# Help Command
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Commands:\n/start - Start chat\n/help - Get help\n/status - Check my status")

# Status Command
def status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("✅ Bot is running smoothly!")

# Handle User Messages & Forward to Flask
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_id = update.message.chat_id

    # Forward message to Flask
    response = requests.post(f"{Config.FLASK_SERVER}/telegram-webhook", json={"user_id": user_id, "message": user_message})
    
    if response.status_code == 200:
        update.message.reply_text("✅ Your message has been received. I will reply soon!")
    else:
        update.message.reply_text("❌ Failed to send your message.")

# Auto-Reply for FAQs
def auto_reply(update: Update, context: CallbackContext) -> None:
    faq_responses = {
        "hello": "Hey there! 👋 How can I help?",
        "pricing": "We offer various cybersecurity services. Check our website for details!",
        "support": "You can contact support at support@kipcodes.com.",
        "contact": "You can reach Kipcodes at @kipngenocodes on Twitter or LinkedIn."
    }
    
    message_text = update.message.text.lower()
    reply = faq_responses.get(message_text, "Sorry, I didn't understand that. Try /help.")
    update.message.reply_text(reply)

# Main Function
def main():
    updater = Updater(Config.TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("status", status))

    # Message Handlers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_reply))

    # Start Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
