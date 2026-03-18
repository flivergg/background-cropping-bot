import json
import os
from datetime import datetime
from config import USER_DATA_FILE

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_stats(user_id):
    data = load_users()
    uid = str(user_id)
    
    if uid not in data:
        data[uid] = {"total": 0, "first": datetime.now().isoformat()}
    
    data[uid]["total"] += 1
    save_users(data)
    return data[uid]