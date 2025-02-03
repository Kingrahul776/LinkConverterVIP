import os
import logging
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Bot Token (Set in Environment or Hardcoded)
BOT1_TOKEN = os.getenv("BOT1_TOKEN", "7918764165:AAFvrPEPc2jEIjy5wTf6S-EZNKq7ol1zZiU")

# ✅ API Endpoint for storing links
API_URL = "https://kingcryptocalls.com/store_link"

# ✅ Initialize the Telegram bot application
app = Application.builder().token(BOT1_TOKEN).build()

# ✅ Start Command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a private Telegram link, and I'll generate a secure short link for you.")

# ✅ Function to generate a short link
def generate_short_link(private_link, user_id):
    try:
        data = {"private_link": private_link, "user_id": user_id}
        response = requests.post(API_URL, json=data)
        logger.info(f"🔗 API Response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                return result["short_link"]
            else:
                return "❌ Error: " + result.get("message", "Unknown error.")
        else:
            return "❌ Error: API request failed."
    except Exception as e:
        logger.error(f"⚠️ Exception in API request: {e}")
        return "❌ Error: Server not responding."

# ✅ Handle user messages (receive private link & generate short link)
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id = update.message.chat_id  # Get the Telegram user ID

    if "t.me/+" in user_message:
        await update.message.reply_text("✅ Link received! Generating your encrypted short link...")
        
        short_link = generate_short_link(user_message, user_id)
        await update.message.reply_text(f"🔗 Your encrypted link: {short_link}")
    else:
        await update.message.reply_text("❌ Please send a valid private Telegram link!")

# ✅ Add Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ✅ Fix for Railway Event Loop Issues
async def run_bot():
    logger.info("🚀 Bot 1 is running...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())  # ✅ Standard execution
    except RuntimeError:
        logger.warning("⚠️ Event loop error detected. Running alternative method.")
        loop = asyncio.get_event_loop()
        loop.create_task(run_bot())
