import os
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Get bot token from environment variables
BOT_TOKEN = os.getenv("7563489228:AAE2srTTgxMD6oNvP1T2SJBVt3nqC0FgNKQ")

# Function to convert a Telegram invite link to a mini-app version
def miniapp_link(invite_link: str) -> str:
    match = re.search(r"https://t.me/\+([\w-]+)", invite_link)
    if match:
        invite_code = match.group(1)
        return f"https://t.me/{invite_code}?start="
    else:
        return "Invalid invite link. Please send a valid Telegram channel invite link."

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a Telegram channel invite link, and I'll convert it into a mini-app version.")

# Handle messages with links
def convert_link(update: Update, context: CallbackContext) -> None:
    invite_link = update.message.text.strip()
    if "t.me/+" in invite_link:
        miniapp_url = miniapp_link(invite_link)
        update.message.reply_text(f"Here’s your Mini-App link: {miniapp_url}")
    else:
        update.message.reply_text("Invalid link. Please send a valid Telegram invite link.")

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_link))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
