from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Your actual BotFather token
BOT_TOKEN = "8229001980:AAEZ1a4AVsq92AOMMEap3tpYwBMgxppgeLQ"

# Anti-link toggle
anti_link_enabled = False

# Command to turn on anti-link
async def antilink_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global anti_link_enabled
    anti_link_enabled = True
    await update.message.reply_text("🛡️ Anti-link is now ON")

# Delete messages with links from non-admins
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not anti_link_enabled:
        return
    message = update.message
    chat = update.effective_chat
    user = message.from_user
    member = await chat.get_member(user.id)
    if member.status in ["administrator", "creator"]:
        return
    if message.entities:
        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                await message.delete()
                break

# Start bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("antilink_on", antilink_on))
    app.add_handler(MessageHandler(filters.ALL, check_message))
    print("Bot is starting...")
    app.run_polling()
