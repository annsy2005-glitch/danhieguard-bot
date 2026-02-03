import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re

BOT_TOKEN = "YOUR_NEW_TOKEN_HERE"

anti_link_enabled = True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is alive ✅")

async def antilink_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link_enabled
    anti_link_enabled = True
    await update.message.reply_text("Anti-link is ON 🔒")

async def antilink_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link_enabled
    anti_link_enabled = False
    await update.message.reply_text("Anti-link is OFF 🔓")

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    user = update.effective_user
    chat = update.effective_chat

    # Log every message (debug)
    print(f"[DEBUG] Message from {user.username if user else 'unknown'}: {message.text}")

    # Skip admins
    member = await chat.get_member(user.id)
    if member.status in ["administrator", "creator"]:
        return

    text = message.text or ""

    # Detect links
    link_pattern = r"(https?://|www\.|t\.me/)"
    if re.search(link_pattern, text.lower()):
        try:
            await message.delete()
            print(f"[DELETED] Link from {user.username}")
        except Exception as e:
            print(f"[ERROR] Failed to delete: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("antilink_on", antilink_on))
    app.add_handler(CommandHandler("antilink_off", antilink_off))
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), check_message))
    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
