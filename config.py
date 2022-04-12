
import os
import logging
from logging.handlers import RotatingFileHandler


# Get a bot token from botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Get from my.telegram.org (or @UseTGXBot)
APP_ID = int(os.environ.get("APP_ID", ))

# Get from my.telegram.org (or @UseTGXBot)
API_HASH = os.environ.get("API_HASH", "")

# Generate a user session string 
TG_USER_SESSION = os.environ.get("TG_USER_SESSION", "---8vZkfZtotQQZySJ1wA")

# Database URL from https://cloud.mongodb.com/
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# Your database name from mongoDB
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# ID of users that can use the bot commands
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "173041").split())

#Small Admins
SM_ADMIN = set(int(x) for x in os.environ.get("SM_ADMIN", "13925").split())

# Should bot search for document files in channels
DOC_SEARCH = os.environ.get("DOC_SEARCH", "no").lower()

#Should bot search for Images
PHO_SEARCH = os.environ.get("PHO_SEARCH", "yes").lower()

# Should bot search for video files in channels
VID_SEARCH = os.environ.get("VID_SEARCH", "no").lower()

# Should bot search for music files in channels
MUSIC_SEARCH = os.environ.get("MUSIC_SEARCH", "no").lower()

#Link of the Channel
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/infinit/")

#Web Site Link
WEB_SITE_URL = os.environ.get("WEB_SITE_URL", "https://www.html?")

#text set when User Request Subtitle
SUB_TEXT = os.environ.get("SUB_TEXT", "𝕊𝕦𝕓𝕥𝕚𝕥𝕝𝕖 ❗️ ")

# Link to File bot url before Array
BOT_URL = os.environ.get("BOT_URL", "https://t.me/SERVERinf_bot?start=")

TG_BOT_SESSION = os.environ.get("TG_BOT_SESSION", "bot")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
LOG_FILE_NAME = "filterbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
