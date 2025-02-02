import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_APP_URL = "https://web-production-8fdb0.up.railway.app"  # ✅ Your Mini-App backend
ADMIN_ID = 6142725643  # ✅ Your Telegram ID

# ✅ Handle "/generate <private_link>" - Generate a secure short link
async def generate_link(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /generate <private_invite_link>")
        return

    private_link = context.args[0]
    response = requests.post(f"{RAILWAY_APP_URL}/create_link", json={"private_link": private_link})
    result = response.json()

    if result["success"]:
        await update.message.reply_text(f"✅ Here is your secure short link:\n{result['short_link']}")
    else:
        await update.message.reply_text("❌ Failed to generate short link.")

# ✅ Main Function
async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("generate", generate_link))

    print("Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(100)

# ✅ Run Bot
if __name__ == "__main__":
    asyncio.run(run_bot())
