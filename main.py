import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Bot Token
BOT1_TOKEN = "YOUR_BOT1_TOKEN_HERE"  # Replace with your actual Bot Token

# ✅ Initialize bot application
app = Application.builder().token(BOT1_TOKEN).build()

# ✅ Start Command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a private link to generate a short link.")

# ✅ Message Handler (Receive Private Links)
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    if "t.me/+" in user_message:
        await update.message.reply_text("✅ Link received! Generating your short link...")
        # Simulate link generation (replace with your API call)
        short_link = f"https://kingcryptocalls.com/short/{hash(user_message) % 100000}"
        await update.message.reply_text(f"🔗 Your short link: {short_link}")
    else:
        await update.message.reply_text("❌ Please send a valid private link!")

# ✅ Add Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ✅ Fix for Event Loop Issue
async def main():
    logger.info("🚀 Bot 1 is running...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            logger.warning("⚠️ Event loop already running. Using alternative start method.")
            loop.create_task(main())  # Non-blocking start
        else:
            loop.run_until_complete(main())  # Standard start
    except RuntimeError:
        asyncio.run(main())  # Fallback method
