import os
from zoneinfo import ZoneInfo
BOT_TOKEN=os.getenv("BOT_TOKEN","")
TIMEZONE=ZoneInfo("Europe/Volgograd")
GROUP_NAME="РКЛ-3"
INSTITUTION="Волжский политехнический техникум"
TIMETABLE_URL="https://volpt.ru/"
DATA_DIR=os.path.join(os.path.dirname(__file__),"data")
DB_PATH=os.path.join(DATA_DIR,"bot.db")
CACHE_TTL_MINUTES=30
MORNING_HOUR=7
MORNING_MINUTE=30
