import time

BLACKLISTED_USERS = set()
user_requests = {}
user_spike_count = {}

MAX_REQUESTS = 10
WINDOW_SECONDS = 5
BLOCK_THRESHOLD = 3

def is_blacklisted(user_id: int) -> bool:
    return user_id in BLACKLISTED_USERS

def is_ddos_or_bot(user_id: int) -> bool:
    now = time.time()
    request_times = user_requests.get(user_id, [])
    request_times = [t for t in request_times if now - t < WINDOW_SECONDS]
    request_times.append(now)
    user_requests[user_id] = request_times

    if len(request_times) > MAX_REQUESTS:
        user_spike_count[user_id] = user_spike_count.get(user_id, 0) + 1
        spike_count = user_spike_count[user_id]
        if spike_count >= BLOCK_THRESHOLD:
            BLACKLISTED_USERS.add(user_id)
            print(f"🚫 User {user_id} permanently blocked for DDoS/spam.")
            return True
        else:
            print(f"⚠️ User {user_id} showing spam behavior. Spike {spike_count}/{BLOCK_THRESHOLD}")
            return True
    return False
