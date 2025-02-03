import os
import logging
import asyncio
import requests
import base64
import hashlib
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Bot Token (Replace with your actual Bot 1 Token)
BOT1_TOKEN = "7918764165:AAFvrPEPc2jEIjy5wTf6S-EZNKq7ol1zZiU"

# ✅ Backend API URL
API_BASE_URL = "https://kingcryptocalls.com"

# ✅ Initialize bot application
app = Application.builder().token(BOT1_TOKEN).build()

# ✅ Function to encrypt the private link securely
def encrypt_link(link):
    hashed = hashlib.sha256(link.encode()).digest()
    return base64.urlsafe_b64encode(hashed).decode()[:10]  # Short but unique

# ✅ Start Command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a private link to generate a short link.")

# ✅ Handle messages containing private links
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id = update.message.from_user.id

    if "t.me/+" in user_message:
        await update.message.reply_text("✅ Link received! Generating your short link...")

        # 🔒 Encrypt the link for security
        short_code = encrypt_link(user_message)

        # 🌍 Store the link via API
        response = requests.post(
            f"{API_BASE_URL}/store_link",
            json={"private_link": user_message, "user_id": user_id},
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            short_link = response.json().get("short_link")
            await update.message.reply_text(f"🔗 Your short link: {short_link}")
        else:
            await update.message.reply_text("❌ Error generating the short link. Please try again.")

    else:
        await update.message.reply_text("❌ Please send a valid private link!")

# ✅ Add Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ✅ Corrected Bot Start for Railway
if __name__ == "__main__":
    logger.info("🚀 Bot 1 is starting...")

    # 🌍 FIX for Railway Event Loop Error
    try:
        import uvloop
        uvloop.install()  # ✅ Use faster event loop (fixes errors in Railway)
    except ImportError:
        logger.warning("⚠️ uvloop not installed, using default event loop.")

    # ✅ Start bot without event loop conflicts
    app.run_polling()
