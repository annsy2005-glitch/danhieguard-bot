import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

LINK_REGEX = re.compile(
    r"(https?://|www\.|t\.me/|telegram\.me/)",
    re.IGNORECASE
)

GROUP_SETTINGS = {}

def is_admin(user_id, admins):
    return user_id in [admin.user.id for admin in admins]

async def antilink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    admins = await context.bot.get_chat_administrators(chat_id)
    if not is_admin(user_id, admins):
        return

    GROUP_SETTINGS.setdefault(chat_id, {})
    GROUP_SETTINGS[chat_id]["antilink"] = (
        context.args and context.args[0].lower() == "on"
    )

    state = "ON" if GROUP_SETTINGS[chat_id]["antilink"] else "OFF"
    await update.message.reply_text(f"🛡️ Anti-link is now {state}")

async def watcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.from_user:
        return

    chat_id = message.chat.id
    user = message.from_user

    settings = GROUP_SETTINGS.get(chat_id, {})
    if not settings.get("antilink"):
        return

    admins = await context.bot.get_chat_administrators(chat_id)
    if is_admin(user.id, admins):
        return

    content = (message.text or "") + (message.caption or "")
    if LINK_REGEX.search(content):
        await message.delete()

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("antilink", antilink))
app.add_handler(MessageHandler(filters.ALL, watcher))
app.run_polling()
