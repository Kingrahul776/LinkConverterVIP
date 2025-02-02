import os
import re
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Get bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to convert a Telegram invite link to a mini-app version
def miniapp_link(invite_link: str) -> str:
    match = re.search(r"https://t.me/\+([\w-]+)", invite_link)
    if match:
        invite_code = match.group(1)
        return f"https://t.me/{invite_code}?start="
    else:
        return "Invalid invite link. Please send a valid Telegram channel invite link."

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a Telegram channel invite link, and I'll convert it into a mini-app version.")

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
    await app.run_polling()

# Ensure the bot runs correctly in Railway
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
