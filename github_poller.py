import asyncio
from multiprocessing import get_logger
import logging
from typing import Any

from github import Github
from github import Auth
import os

from telegram._bot import BT
from telegram.error import TimedOut
from telegram.ext import CallbackContext, ExtBot, Application
from telegram.ext._utils.types import CCT, UD, CD, BD

logger = logging.getLogger(__name__)


class WebhookUpdate:
    user_id: int
    payload: str


class GitHubIssuePoller:
    chats = []

    def __init__(self, application: "Application[BT, CCT, UD, CD, BD, Any]"):
        with open("chats.txt") as f:
            for line in f.readlines():
                self.chats.append(int(line))
        self.running = True
        self.issues = None
        token = os.environ['GH_TOKEN']
        self.auth = Auth.Token(token)
        self.g = Github(auth=self.auth)
        self.repo = self.g.get_repo('boriskhodok/wowsuptime')
        self.application = application

    async def poll_issues(self):
        while self.running:
            logger.info("Polling issues")
            try:
                self.issues = self.repo.get_issues(state='open', labels=["status"])
                if len(self.chats) > 0:
                    for chat_id in self.chats:
                        for issue in self.issues:
                            message = issue.title + "\n\n"
                            message += issue.body
                            await self.application.bot.send_message(chat_id, message,
                                                                    parse_mode="Markdown",
                                                                    disable_web_page_preview=True)
                            await asyncio.sleep(1)
                logger.info("Got issues: " + str(self.issues.totalCount))
            except Exception as e:
                logger.error("Exception: " + str(type(e)) + " " + e.message)
            await asyncio.sleep(30)

    @classmethod
    def add_chat(cls, chat_id: int):
        with open("chats.txt", "a") as f:
            if chat_id not in cls.chats:
                cls.chats.append(chat_id)
                f.write(str(chat_id))

    async def shutdown(self) -> None:
        if self.running:
            raise RuntimeError("This Poller is still running!")

        self.running = False
        logger.debug("Shut down of Poller complete")
