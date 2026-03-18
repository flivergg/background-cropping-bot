import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
USER_DATA_FILE = "user_data.json"

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}