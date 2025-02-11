from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from config import Config
import asyncio

# Start Command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Hello! I am Kipcodes' bot. Send me a message and I'll reply!")

# Help Command
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Commands:\n/start - Start chat\n/help - Get help\n/status - Check my status")

# Status Command
async def status(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("✅ Bot is running smoothly!")

# Handle User Messages & Forward to Flask
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_id = update.message.chat_id

    # Forward message to Flask backend
    response = requests.post(f"{Config.FLASK_SERVER}/telegram-webhook", json={"user_id": user_id, "message": user_message})
    
    if response.status_code == 200:
        await update.message.reply_text("✅ Your message has been received. I will reply soon!")
    else:
        await update.message.reply_text("❌ Failed to send your message.")

# Auto-Reply for FAQs
async def auto_reply(update: Update, context: CallbackContext) -> None:
    faq_responses = {
        "hello": "Hey there! 👋 How can I help?",
        "pricing": "We offer various cybersecurity services. Check our website for details!",
        "support": "You can contact support at support@kipcodes.com.",
        "contact": "You can reach Kipcodes at @kipngenocodes on Twitter or LinkedIn."
    }
    
    message_text = update.message.text.lower()
    reply = faq_responses.get(message_text, "Sorry, I didn't understand that. Try /help.")
    await update.message.reply_text(reply)

# Main Function
async def main():
    app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))

    # Message Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    # Start Bot
    print("🚀 Telegram Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
