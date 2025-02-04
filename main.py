import os
import logging
import requests
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Fix Event Loop Issues
nest_asyncio.apply()

# ✅ Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Bot Token & API URL
BOT1_TOKEN = "7918764165:AAFvrPEPc2jEIjy5wTf6S-EZNKq7ol1zZiU"
API_URL = "https://kingcryptocalls.com/store_link"
ADMIN_ID = 6142725643  # ✅ Admin ID

# ✅ Initialize Bot
app = Application.builder().token(BOT1_TOKEN).build()

# ✅ Delete Webhook to Avoid Conflicts
async def delete_webhook():
    url = f"https://api.telegram.org/bot{BOT1_TOKEN}/deleteWebhook"
    response = requests.post(url)
    if response.json().get("ok"):
        logger.info("✅ Webhook deleted successfully.")
    else:
        logger.warning("⚠️ Webhook deletion failed.")

# ✅ Start Command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Send me a private Telegram link, and I'll generate an encrypted link.")

# ✅ Handle Messages (Generate Short Link)
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id = str(update.message.from_user.id)

    if "t.me/+" in user_message:
        await update.message.reply_text("🔄 Processing your link...")

        # ✅ Allow Admin (6142725643) to generate links without a subscription
        if user_id == "6142725643":
            payload = {"private_link": user_message, "user_id": user_id}
            headers = {"Content-Type": "application/json"}
            response = requests.post(API_URL, json=payload, headers=headers)
            data = response.json()

            if data["success"]:
                await update.message.reply_text(f"✅ Your encrypted link:\n👉 {data['short_link']}")
            else:
                await update.message.reply_text(f"❌ {data['message']}")
            return  # Exit function for admin users

        # ✅ Check subscription for normal users
        payload = {"private_link": user_message, "user_id": user_id}
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()

        if data["success"]:
            await update.message.reply_text(f"✅ Your encrypted link:\n👉 {data['short_link']}")
        else:
            await update.message.reply_text(f"❌ {data['message']}")
    else:
        await update.message.reply_text("❌ Invalid link! Please send a **private Telegram invite link**.")


# ✅ Add Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ✅ Run Bot
async def run_bot():
    logger.info("🚀 Bot 1 is starting...")
    await delete_webhook()
    await app.initialize()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(run_bot())
