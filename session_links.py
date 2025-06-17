import time

# Stores uid → (url, timestamp)
insta_links = {}
EXPIRY_SECONDS = 300  # 5 minutes

def set_link(uid: str, url: str):
    """Save the Instagram link with timestamp."""
    insta_links[uid] = (url, time.time())

def get_link(uid: str):
    """Retrieve the link if not expired."""
    data = insta_links.get(uid)
    if not data:
        return None

    url, timestamp = data
    if time.time() - timestamp > EXPIRY_SECONDS:
        del insta_links[uid]  # Expired
        return None

    return url