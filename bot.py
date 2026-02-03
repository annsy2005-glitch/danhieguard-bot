BOT_TOKEN = "8229001980:AAEZ1a4AVsq92AOMMEap3tpYwBMgxppgeLQ"

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re

# Anti-link toggle
anti_link_enabled = False

# Command to turn anti-link ON
async def antilink_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link_enabled
    anti_link_enabled = True
    await update.message.reply_text("🛡️ Anti-link is now ON")
    print(f"[INFO] Anti-link enabled by {update.message.from_user.username}")

# Command to turn anti-link OFF
async def antilink_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link_enabled
    anti_link_enabled = False
    await update.message.reply_text("🛡️ Anti-link is now OFF")
    print(f"[INFO] Anti-link disabled by {update.message.from_user.username}")

# Check messages for links
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not anti_link_enabled:
        return

    message = update.message
    if not message:
        return
    chat = update.effective_chat
    user = message.from_user
    member = await chat.get_member(user.id)

    # Skip admins and owner
    if member.status in ["administrator", "creator"]:
        return

    text = message.text or ""
    # Regex to detect links
    link_pattern = r"(https?://\S+|www\.\S+)"
    if re.search(link_pattern, text):
        print(f"[LINK FOUND] From {user.username}: {text}")
        try:
            await message.delete()
            print(f"[DELETED] Link from {user.username}")
        except Exception as e:
            print(f"[ERROR] Failed to delete message from {user.username}: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("antilink_on", antilink_on))
    app.add_handler(CommandHandler("antilink_off", antilink_off))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_message))
    print("Bot is starting...")
    app.run_polling()
