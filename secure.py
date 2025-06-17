from config import ALLOWED_USERS

def is_authorized(user_id):
    return not ALLOWED_USERS or user_id in ALLOWED_USERS