import os
import re
import random
import string
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_APP_URL = "https://web-production-8fdb0.up.railway.app"  # ✅ Temporary Railway domain

# Function to generate a random short code
def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to store and get a random short link
def miniapp_link(invite_link: str) -> str:
    match = re.search(r"https://t\.me/\+([\w-]+)", invite_link)
    if match:
        invite_code = match.group(1)
        short_code = generate_random_code()

        print(f"[DEBUG] Generated short code: {short_code} for invite: {invite_code}")

        # Store the short link in the redirect server
        SHORTENER_API = f"{RAILWAY_APP_URL}/store"
        try:
            response = requests.post(SHORTENER_API, json={"code": short_code, "target": f"https://t.me/+{invite_code}"})
            response_json = response.json()

            print(f"[DEBUG] Response from shortener: {response_json}")

            if response.status_code == 200:
                return f"{RAILWAY_APP_URL}/{short_code}"  # ✅ Temporary Railway domain
            else:
                return f"Error: Received status {response.status_code} from the shortener."

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to connect to shortener: {e}")
            return "Error: Could not generate short link."

    else:
        return "Invalid invite link. Please send a valid Telegram invite link."

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a Telegram channel invite link, and I'll convert it into a random short link.")

# Handle messages with links
async def convert_link(update: Update, context: CallbackContext) -> None:
    invite_link = update.message.text.strip()
    if "t.me/+" in invite_link:
        miniapp_url = miniapp_link(invite_link)
        print(f"[DEBUG] Sending Mini-App link: {miniapp_url}")
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
