import os
from dotenv import load_dotenv

load_dotenv()

BOT_API = os.getenv("TG_BOT_TOKEN")
SEARCH_API = os.getenv("SEARCH_API")
SEARCH_ID = os.getenv("SEARCH_ID")
KINOPOISK_API = os.getenv("KINOPOISK_API")