import os import time import threading import logging from telegram.error import Forbidden, TelegramError

✅ Auto delete any file after delay (default = 300 seconds)

def auto_delete(file_path, delay=300): def delete_file(): time.sleep(delay) if os.path.exists(file_path): os.remove(file_path) logging.info(f"🧹 Deleted: {file_path}") threading.Thread(target=delete_file).start()

✅ Safe send message to prevent crash if user blocks the bot

def log_blocked_user(user_id): try: with open("logs/blocked.txt", "r") as f: blocked = f.read().splitlines() if str(user_id) not in blocked: with open("logs/blocked.txt", "a") as f: f.write(str(user_id) + "\n") except FileNotFoundError: with open("logs/blocked.txt", "w") as f: f.write(str(user_id) + "\n")

# Increment block count
count_file = "logs/block_count.txt"
count = {}
try:
    with open(count_file, "r") as f:
        for line in f:
            uid, c = line.strip().split(":")
            count[uid] = int(c)
except FileNotFoundError:
    pass

user_id_str = str(user_id)
count[user_id_str] = count.get(user_id_str, 0) + 1

# Write updated count
with open(count_file, "w") as f:
    for uid, c in count.items():
        f.write(f"{uid}:{c}\n")

# If blocked 3 times, permanently ban
if count[user_id_str] >= 3:
    with open("logs/blocked.txt", "a") as f:
        f.write(str(user_id) + "\n")

async def safe_send(bot, user_id, text, **kwargs): try: await bot.send_message(chat_id=user_id, text=text, **kwargs) except Forbidden: logging.warning(f"🚫 User {user_id} blocked the bot.") log_blocked_user(user_id) except TelegramError as e: logging.error(f"⚠️ Telegram error for user {user_id}: {e}") except Exception as e: logging.error(f"❌ Unknown error sending message to {user_id}: {e}")