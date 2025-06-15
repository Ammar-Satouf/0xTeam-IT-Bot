import json
import os

NOTIFIED_USERS_FILE = "notified_users.json"

def load_notified_users():
    if os.path.exists(NOTIFIED_USERS_FILE):
        with open(NOTIFIED_USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_notified_users(user_ids):
    with open(NOTIFIED_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(user_ids, f, indent=4, ensure_ascii=False)
