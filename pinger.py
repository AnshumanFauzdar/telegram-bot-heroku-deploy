import asyncio
import logging
import time
from datetime import datetime

import aiohttp
import yaml
from telegram.ext import Application
from yaml import Loader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def _process_sites(sites):
    processed_sites = {}
    for site in sites:
        processed_sites[site["name"]] = {}
        processed_sites[site["name"]]["url"] = site["url"]
        processed_sites[site["name"]]["isUp"] = False
        processed_sites[site["name"]]["responseStatus"] = 0
        processed_sites[site["name"]]["responseTime"] = 0
        processed_sites[site["name"]]["downSince"] = datetime.now()
    return processed_sites


def diff_minutes_round(date1: datetime, date2: datetime) -> int:
    diff = (date1 - date2).seconds / 60
    return abs(round(diff))


class SitePinger:
    chats = []

    def __init__(self, application: Application):
        self.running = True
        with open("chats.txt") as f:
            for line in f.readlines():
                self.chats.append(int(line))

        self.semaphore = asyncio.Semaphore(10)

        self.sites = _process_sites(yaml.load(open("sites.yml"), Loader=Loader)["sites"])
        self.application = application

    async def check_sites_and_send_message(self):
        for name in self.sites.keys():
            down_since_diff = diff_minutes_round(datetime.now(), self.sites[name]["downSince"])
            if not self.sites[name]["isUp"]:
                if down_since_diff > 15:
                    self.sites[name]["downSince"] = datetime.now()
                    message = "🛑 " + self.sites[name]["url"] + " is down"
                    await self._send_message_to_chats(message)
        await asyncio.sleep(300)

    async def ping_sites(self):
        while self.running:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    for name in self.sites.keys():
                        await self._ping_site(name, session)
            await asyncio.sleep(300)

    async def _ping_site(self, name, session):
        try:
            start = time.monotonic()
            r = await session.get(self.sites[name]["url"])
            status = r.status
            response_time = int(round(time.monotonic() - start, 3) * 1000)
            self.sites[name]["responseStatus"] = status
            if status < 500:
                if not self.sites[name]["isUp"]:
                    message = "🟢 " + self.sites[name]["url"] + " is up"
                    await self._send_message_to_chats(message)
                self.sites[name]["isUp"] = True
            else:
                if self.sites[name]["isUp"]:
                    message = "🛑 " + self.sites[name]["url"] + " is down (Server Error)"
                    await self._send_message_to_chats(message)
                self.sites[name]["isUp"] = False
            self.sites[name]["responseTime"] = response_time
            logger.info(str(status) + " " + str(response_time) + " " + self.sites[name]["url"])
        except Exception as e:
            if self.sites[name]["isUp"]:
                message = "🛑 " + self.sites[name]["url"] + " is down"
                await self._send_message_to_chats(message)
            self.sites[name]["isUp"] = False
            self.sites[name]["responseTime"] = 0
            logger.error(str(e) + " " + self.sites[name]["url"])

    async def _send_message_to_chat(self, chat_id, message):
        await self.application.bot.send_message(chat_id, message,
                                                disable_web_page_preview=True)
        await asyncio.sleep(5)

    @classmethod
    def add_chat(cls, chat_id: int):
        with open("chats.txt", "a") as f:
            if chat_id not in cls.chats:
                cls.chats.append(chat_id)
                f.write(str(chat_id))

    async def _send_message_to_chats(self, message):
        for chat_id in self.chats:
            await self._send_message_to_chat(chat_id, message)
