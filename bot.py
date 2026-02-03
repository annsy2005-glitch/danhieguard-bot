BOT_TOKEN = "8229001980:AAEZ1a4AVsq92AOMMEap3tpYwBMgxppgeLQ"

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Toggle for anti-link
anti_link_enabled = False

# Command to turn anti-link ON
async def antilink_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link_enabled
    anti_link_enabled = True
    await update.message.reply_text("🛡️ Anti-link is now ON")

# Command to turn anti-link OFF (optional)
async def antilink_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link_enabled
    anti_link_enabled = False
    await update.message.reply_text("🛡️ Anti-link is now OFF")

# Check every message
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Message received from {update.message.from_user.username}: {update.message.text}")
    # Skip admins and group owner
    if member.status in ["administrator", "creator"]:
        return
    # Delete if message contains link
    if message.entities:
        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                await message.delete()
                break

# Start bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("antilink_on", antilink_on))
    app.add_handler(CommandHandler("antilink_off", antilink_off))
    app.add_handler(MessageHandler(filters.ALL, check_message))
    print("Bot is starting...")
    app.run_polling()
