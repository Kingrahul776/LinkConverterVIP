import os
import random
import string
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

BOT1_TOKEN = os.getenv("BOT1_TOKEN")  # ✅ Token for Bot 1
BOT2_USERNAME = "vipsignals221bot"  # 🔹 Replace with your Bot 2 username
RAILWAY_APP_URL = "https://web-production-8fdb0.up.railway.app"  # ✅ Your backend URL
ADMIN_ID = 6142725643  # ✅ Your Telegram ID

# ✅ Generate a random short code
def generate_short_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ Handle "/generate <private_link>" to create a short link
async def generate_link(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /generate <private_invite_link>")
        return

    private_link = context.args[0]
    short_code = generate_short_code()
    short_url = f"https://t.me/{BOT2_USERNAME}?start={short_code}"

    # ✅ Store the mapping in the backend
    requests.post(f"{RAILWAY_APP_URL}/store_link", json={"short_code": short_code, "private_link": private_link})

    await update.message.reply_text(f"✅ Here is your short link:\n{short_url}")

# ✅ Main Function
async def run_bot():
    app = Application.builder().token(BOT1_TOKEN).build()
    app.add_handler(CommandHandler("generate", generate_link))

    print("Bot 1 is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(100)

if __name__ == "__main__":
    asyncio.run(run_bot())
