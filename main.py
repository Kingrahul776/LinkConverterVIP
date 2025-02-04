import os
import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Bot Token (Replace with actual)
BOT1_TOKEN = "7918764165:AAFvrPEPc2jEIjy5wTf6S-EZNKq7ol1zZiU"
API_URL = "https://kingcryptocalls.com/store_link"

# ✅ Initialize Telegram Bot
app = Application.builder().token(BOT1_TOKEN).build()

# ✅ Start Command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Welcome! Send me a private Telegram link, and I'll generate an encrypted link.")

# ✅ Handle Messages (Generate Short Link)
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id = update.message.from_user.id

    if "t.me/+" in user_message:
        await update.message.reply_text("🔄 Processing your link...")
        
        # ✅ API Call to Generate Short Link
        payload = {"private_link": user_message, "user_id": str(user_id)}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            data = response.json()

            if data["success"]:
                short_link = data["short_link"]
                await update.message.reply_text(f"✅ Your encrypted link:\n👉 {short_link}")
            else:
                await update.message.reply_text(f"❌ {data['message']}")
        except Exception as e:
            logger.error(f"Error generating link: {e}")
            await update.message.reply_text("⚠️ Error generating the short link. Please try again.")
    else:
        await update.message.reply_text("❌ Invalid link! Please send a **private Telegram invite link**.")

# ✅ Add Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ✅ Run Bot
async def run_bot():
    logger.info("🚀 Bot 1 is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(run_bot())
