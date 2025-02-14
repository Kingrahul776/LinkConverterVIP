import os
import logging
import requests
import asyncio
import nest_asyncio  # ✅ Fixes event loop errors!
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Apply fix for "RuntimeError: Event loop is already running"
nest_asyncio.apply()

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Bot Token (Replace with actual)
BOT1_TOKEN = "7918764165:AAFvrPEPc2jEIjy5wTf6S-EZNKq7ol1zZiU"
API_URL = "https://web-production-8fdb0.up.railway.app/store_link"

# ✅ Initialize Telegram Bot
app = Application.builder().token(BOT1_TOKEN).build()

# ✅ Delete any existing webhook to avoid conflicts
async def delete_webhook():
    url = f"https://api.telegram.org/bot{BOT1_TOKEN}/deleteWebhook"
    try:
        response = requests.post(url)
        data = response.json()
        if data.get("ok"):
            logger.info("✅ Webhook deleted successfully.")
        else:
            logger.warning("⚠️ Webhook deletion failed.")
    except Exception as e:
        logger.error(f"❌ Error deleting webhook: {e}")

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

            # ✅ Log API Response for debugging
            logger.info(f"API Response: {data}")

            if data.get("success"):
                short_link = data.get("short_link")
                await update.message.reply_text(f"✅ Your encrypted link:\n👉 {short_link}")
            else:
                await update.message.reply_text(f"❌ {data.get('message')}")
        except Exception as e:
            logger.error(f"Error generating link: {e}")
            await update.message.reply_text("⚠️ Error generating the short link. Please try again.")
    else:
        await update.message.reply_text("❌ Invalid link! Please send a **private Telegram invite link**.")

# ✅ Add Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ✅ Run Bot with Proper Event Loop Handling
async def run_bot():
    logger.info("🚀 Bot 1 is starting...")
    await delete_webhook()  # Ensure webhook is removed before starting polling
    await app.initialize()
    await app.run_polling()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            logger.warning("⚠️ Event loop already running. Running bot in a new task.")
            loop.create_task(run_bot())
        else:
            loop.run_until_complete(run_bot())
    except RuntimeError as e:
        if "no running event loop" in str(e):
            asyncio.run(run_bot())
        else:
            logger.error(f"❌ Unexpected error: {e}")
