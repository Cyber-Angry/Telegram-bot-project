import time

insta_links = {}
EXPIRY_SECONDS = 300

def set_link(uid: str, url: str):
    insta_links[uid] = (url, time.time())

def get_link(uid: str):
    data = insta_links.get(uid)
    if not data:
        return None
    url, timestamp = data
    if time.time() - timestamp > EXPIRY_SECONDS:
        del insta_links[uid]
        return None
    return url
