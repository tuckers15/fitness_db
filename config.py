import os
from dotenv import load_dotenv

#load environmental variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}
