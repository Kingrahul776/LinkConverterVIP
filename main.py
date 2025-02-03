import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters

# ✅ Hardcoded Telegram Bot Token (Replace with your actual token)
BOT1_TOKEN = "7563489228:AAFbHt27pZxUZVa3e3il0G7YypthgnREWkg"

# ✅ API Endpoint (Change if needed)
API_BASE_URL = "https://kingcryptocalls.com"

# ✅ Admin Telegram User ID
ADMINS = ["6142725643"]  # Add more if needed

# ✅ Initialize the Bot
app = Application.builder().token(BOT1_TOKEN).build()

# ✅ Command: Start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Welcome! Use /generate <private_link> to create an encrypted invite link.")

# ✅ Command: Generate Encrypted Link
async def generate(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /generate <private_link>")
        return
    
    user_id = str(update.message.from_user.id)
    private_link = context.args[0]

    payload = {"private_link": private_link, "user_id": user_id}
    response = requests.post(f"{API_BASE_URL}/store_link", json=payload)

    data = response.json()
    if data["success"]:
        await update.message.reply_text(f"✅ Your encrypted link: {data['short_link']}")
    else:
        await update.message.reply_text(f"❌ Error: {data['message']}")

# ✅ Command (Admin Only): Subscribe a User
async def subscribe(update: Update, context: CallbackContext):
    if str(update.message.from_user.id) not in ADMINS:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /subscribe <user_id> <days>")
        return

    user_id = context.args[0]
    days = int(context.args[1])

    payload = {"user_id": user_id, "days": days}
    response = requests.post(f"{API_BASE_URL}/add_subscription", json=payload)

    data = response.json()
    await update.message.reply_text(data["message"])

# ✅ Command: Check Subscription Status
async def check_subscription(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    response = requests.get(f"{API_BASE_URL}/check_subscription?user_id={user_id}")
    data = response.json()

    if data["success"]:
        await update.message.reply_text(f"✅ You have an active subscription until {data['expiry_date']}")
    else:
        await update.message.reply_text("❌ You do not have an active subscription.")

# ✅ Command (Admin Only): List All Subscribers (Future Feature)
async def list_subscriptions(update: Update, context: CallbackContext):
    if str(update.message.from_user.id) not in ADMINS:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    await update.message.reply_text("⚠️ Listing all subscribers is not implemented yet.")

# ✅ Register Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("generate", generate))
app.add_handler(CommandHandler("subscribe", subscribe))
app.add_handler(CommandHandler("checksub", check_subscription))
app.add_handler(CommandHandler("listsubs", list_subscriptions))

# ✅ Start the Bot (Fix for Asyncio RuntimeError)
async def run_bot():
    print("🚀 Bot 1 is starting...")
    await app.run_polling()

if __name__ == "__main__":
    print("🚀 Bot 1 is initializing...")

    try:
        asyncio.run(run_bot())  # ✅ This properly starts the bot
    except RuntimeError:
        print("⚠️ Event loop already running. Using alternative method.")
        loop = asyncio.get_event_loop()
        loop.create_task(run_bot())  # ✅ Keeps bot running
        loop.run_forever()
