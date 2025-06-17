import os

os.makedirs("logs", exist_ok=True)
for file in ["users.txt", "blocked.txt", "block_count.txt"]:
    open(f"logs/{file}", "a").close()

USERS_FILE = "logs/users.txt"
BLOCKED_FILE = "logs/blocked.txt"
BLOCK_COUNT_FILE = "logs/block_count.txt"

def log_user(user_id):
    user_id = str(user_id)
    with open(USERS_FILE, "r+") as f:
        users = f.read().splitlines()
        if user_id not in users:
            f.write(user_id + "\n")

def is_banned(user_id):
    user_id = str(user_id)
    with open(BLOCKED_FILE, "r") as f:
        return user_id in f.read().splitlines()

def handle_bot_block(user_id):
    user_id = str(user_id)
    counts = {}
    with open(BLOCK_COUNT_FILE, "r+") as f:
        lines = f.read().splitlines()
        for line in lines:
            uid, count = line.split(":")
            counts[uid] = int(count)

    current_count = counts.get(user_id, 0) + 1
    counts[user_id] = current_count

    with open(BLOCK_COUNT_FILE, "w") as f:
        for uid, count in counts.items():
            f.write(f"{uid}:{count}\n")

    if current_count >= 3:
        with open(BLOCKED_FILE, "r+") as f:
            blocked = f.read().splitlines()
            if user_id not in blocked:
                f.write(user_id + "\n")
        return True
    return False
