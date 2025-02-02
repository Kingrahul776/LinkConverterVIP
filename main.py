import os
import re
import random
import string
import asyncio
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_APP_URL = "https://web-production-8fdb0.up.railway.app"  # ✅ Your Mini-App on Railway
SUBSCRIBERS_FILE = "subscribers.json"  # ✅ Stores user data
ADMIN_ID = 6142725643  # ✅ Your Telegram ID

# ✅ Load Subscribers
def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# ✅ Save Subscribers
def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subscribers, f)

# ✅ Generate a Random Tracking Code
def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ Handle "/start xyz123" - When Users Click the Bot Link
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    args = context.args  # Get the tracking code from the link

    subscribers = load_subscribers()

    # ✅ Store user if not already added
    if str(user_id) not in subscribers:
        subscribers[str(user_id)] = {"username": user_name, "ref_code": args[0] if args else "direct"}
        save_subscribers(subscribers)

    # ✅ Generate a mini-app redirection link
    miniapp_redirect_url = f"{RAILWAY_APP_URL}/redirect?user_id={user_id}"

    # ✅ Send mini-app link for instant redirection
    await update.message.reply_text(
        f"🎉 Welcome! Redirecting you to the channel...\n"
        f"➡️ [Click here]({miniapp_redirect_url}) to continue.",
        parse_mode="Markdown"
    )

# ✅ Generate Tracking Link
async def get_tracking_link(update: Update, context: CallbackContext) -> None:
    tracking_code = generate_random_code()
    bot_username = context.bot.username
    tracking_link = f"https://t.me/{bot_username}?start={tracking_code}"
    
    await update.message.reply_text(f"✅ Here is your tracking link: {tracking_link}")

# ✅ Broadcast Message to Collected Users (Only Admin)
async def broadcast(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    subscribers = load_subscribers()
    count = 0

    for user_id in subscribers:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            count += 1
        except Exception as e:
            print(f"[ERROR] Failed to send message to {user_id}: {e}")

    await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

# ✅ Main Function
async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getlink", get_tracking_link))
    app.add_handler(CommandHandler("broadcast", broadcast))

    print("Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(100)

# ✅ Run Bot
if __name__ == "__main__":
    asyncio.run(run_bot())
