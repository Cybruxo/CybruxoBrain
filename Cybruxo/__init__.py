# Copyright (c) 2026 Cybruxo
# Licensed under the MIT License.
# This file is part of CYBRUXO 


import time
import asyncio
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


__version__ = "3.0.3"

from config import Config

config = Config()
config.check()
tasks = []
boot = time.time()

from Cybruxo.core.bot import Bot
app = Bot()

from Cybruxo.core.dir import ensure_dirs
ensure_dirs()

from Cybruxo.core.userbot import Userbot
userbot = Userbot()

from Cybruxo.core.mongo import MongoDB
db = MongoDB()

from Cybruxo.core.lang import Language
lang = Language()

from Cybruxo.core.telegram import Telegram
from Cybruxo.core.youtube import YouTube
tg = Telegram()
yt = YouTube()

from Cybruxo.helpers import Queue, Thumbnail
queue = Queue()
thumb = Thumbnail()

from Cybruxo.core.calls import TgCall
anon = TgCall()


async def stop() -> None:
    logger.info("Stopping...")
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.exceptions.CancelledError:
            pass

    await app.exit()
    await userbot.exit()
    await db.close()
    await thumb.close()

    logger.info("Stopped.\n")
