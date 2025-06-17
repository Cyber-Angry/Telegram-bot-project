import time

# 🚫 Set of permanently blocked users
BLACKLISTED_USERS = set()

# 🛡️ Track per-user requests
user_requests = {}
user_spike_count = {}

# 🔧 Settings
MAX_REQUESTS = 10         # Max allowed requests in short burst
WINDOW_SECONDS = 5        # Time window to monitor spikes
BLOCK_THRESHOLD = 3       # Spikes before permanent block

def is_blacklisted(user_id: int) -> bool:
    """Check if the user is blacklisted permanently."""
    return user_id in BLACKLISTED_USERS

def is_ddos_or_bot(user_id: int) -> bool:
    """
    Check for DDoS-like behavior and rate-limiting abuse.
    Temporarily warns on repeated rapid requests, permanently blocks after threshold.
    """
    now = time.time()
    request_times = user_requests.get(user_id, [])

    # Remove outdated entries
    request_times = [t for t in request_times if now - t < WINDOW_SECONDS]
    request_times.append(now)
    user_requests[user_id] = request_times

    # Check request frequency
    if len(request_times) > MAX_REQUESTS:
        user_spike_count[user_id] = user_spike_count.get(user_id, 0) + 1
        spike_count = user_spike_count[user_id]

        if spike_count >= BLOCK_THRESHOLD:
            BLACKLISTED_USERS.add(user_id)
            print(f"🚫 User {user_id} permanently blocked for DDoS/spam.")
            return True  # Blocked
        else:
            print(f"⚠️ User {user_id} showing spam behavior. Spike {spike_count}/{BLOCK_THRESHOLD}")
            return True  # Warning stage
    return False