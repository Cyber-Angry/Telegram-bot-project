import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv
from instagram import build_instagram_buttons, download_instagram_format
from session_links import insta_links, set_link
from security import is_blacklisted, is_ddos_or_bot
from user_logger import log_user

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = ["@oxAngry", "@modflux_99"]

logging.basicConfig(level=logging.INFO)

BOT_DESCRIPTION = """👋 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙏𝙤 𝙄𝙣𝙨𝙩𝙖𝙏𝙪𝙗𝙚𝘽𝙤𝙩 📥
━━━━━━━━━━━━━━━━━━━
🎬 𝗢𝗻𝗲-𝗧𝗮𝗽 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗥𝗲𝗲𝗹𝘀 & 𝗦𝘁𝗼𝗿𝗶𝗲𝘀 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿
🔹 Download Reels, Stories & MP3 Audio
🔹 Auto Detect Instagram Links
🔹 Direct High Quality File Output
"""

def get_force_join_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Join @oxAngry", url="https://t.me/oxAngry")],
        [InlineKeyboardButton("🔗 Join @modflux_99", url="https://t.me/modflux_99")],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_subscription")]
    ])

async def check_membership(user_id, context):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    user_id = update.effective_user.id
    log_user(user_id)
    if not await check_membership(user_id, context):
        await update.message.reply_text("🔒 Please join both channels to use this bot.", reply_markup=get_force_join_buttons())
        return
    await update.message.reply_text(BOT_DESCRIPTION)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_subscription":
        if await check_membership(user_id, context):
            await query.edit_message_text("✅ Access granted! Now send an Instagram link.")
            await context.bot.send_message(chat_id=user_id, text=BOT_DESCRIPTION)
        else:
            await query.edit_message_text("❌ You're still not in both channels. Join them first.", reply_markup=get_force_join_buttons())
        return

    try:
        tag, quality, uid = query.data.split("|", 2)
        await query.edit_message_text("📥 Downloading your video/audio, please wait...")

        if tag == "insta":
            url = insta_links.get(uid)
            if not url:
                await query.message.reply_text("⚠️ Link expired or not found.")
                return
            file_path = download_instagram_format(url, quality)

            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    await query.message.reply_document(document=f)
                os.remove(file_path)
            else:
                await query.message.reply_text("❌ Failed to download. Please try again later.")
    except Exception as e:
        logging.error(f"[ButtonHandler] Download error: {e}")
        await query.message.reply_text("❌ Internal error occurred.")

async def handle_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    user_id = update.effective_user.id
    log_user(user_id)

    if is_blacklisted(user_id):
        await update.message.reply_text("🚫 You're permanently blocked due to abuse.")
        return

    if is_ddos_or_bot(user_id):
        await update.message.reply_text("⚠️ Suspicious activity detected. Stop spamming or you'll be blocked!")
        return

    if not await check_membership(user_id, context):
        await update.message.reply_text("🔒 Please join both channels first.", reply_markup=get_force_join_buttons())
        return

    message = update.message.text
    if "instagram.com" in message:
        try:
            uid = str(user_id)
            set_link(uid, message)
            buttons = build_instagram_buttons(message, uid)
            await update.message.reply_text("🎯 Choose the format:", reply_markup=buttons)
        except Exception as e:
            logging.error(f"[HandleLinks] Error building buttons: {e}")
            await update.message.reply_text("⚠️ Failed to process link.")
    else:
        await update.message.reply_text("❌ Please send a valid Instagram link.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, handle_links))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Bot running...")
    app.run_polling()
