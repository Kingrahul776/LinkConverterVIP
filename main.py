import os
import re
import random
import string
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHORTENER_API = "https://www.kingcryptocalls.com/store"  # Your domain for short links

# Function to generate a random short code
def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to store and get a random short link
def miniapp_link(invite_link: str) -> str:
    match = re.search(r"https://t\.me/\+([\w-]+)", invite_link)
    if match:
        invite_code = match.group(1)
        short_code = generate_random_code()

        # Store the short link in the redirect server
        response = requests.post(SHORTENER_API, json={"code": short_code, "target": f"https://t.me/+{invite_code}"})

        if response.status_code == 200:
            return f"https://www.kingcryptocalls.com/{short_code}"
        else:
            return "Error generating short link."

    else:
        return "Invalid invite link. Please send a valid Telegram channel invite link."

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a Telegram channel invite link, and I'll convert it into a random short link.")

# Handle messages with links
async def convert_link(update: Update, context: CallbackContext) -> None:
    invite_link = update.message.text.strip()
    if "t.me/+" in invite_link:
        miniapp_url = miniapp_link(invite_link)
        await update.message.reply_text(f"Here’s your Mini-App link: {miniapp_url}")
    else:
        await update.message.reply_text("Invalid link. Please send a valid Telegram invite link.")

# Main function
async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))

    print("Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(100)

# Run bot on Railway
if __name__ == "__main__":
    asyncio.run(run_bot())  # ✅ Works properly now
