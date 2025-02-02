import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# ✅ Load token from environment variable
BOT1_TOKEN = os.getenv("BOT1_TOKEN")
if not BOT1_TOKEN:
    raise ValueError("🚨 ERROR: BOT1_TOKEN is missing! Set it in Railway.")

RAILWAY_APP_URL = "https://web-production-8fdb0.up.railway.app"  # ✅ Backend URL
ADMIN_ID = 6142725643  # ✅ Your Telegram ID

# ✅ Handle "/generate <private_link>" to create an encrypted short link
async def generate_link(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /generate <private_invite_link>")
        return

    private_link = context.args[0]
    response = requests.post(f"{RAILWAY_APP_URL}/store_link", json={"private_link": private_link})
    result = response.json()

    if result["success"]:
        await update.message.reply_text(f"✅ Here is your encrypted short link:\n{result['short_link']}")
    else:
        await update.message.reply_text("❌ Failed to generate short link.")

# ✅ Main Function
async def run_bot():
    app = Application.builder().token(BOT1_TOKEN).build()
    app.add_handler(CommandHandler("generate", generate_link))

    print("🚀 Bot 1 is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(100)

if __name__ == "__main__":
    asyncio.run(run_bot())
