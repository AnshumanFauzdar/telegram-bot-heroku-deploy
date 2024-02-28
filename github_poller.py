import asyncio
import logging
import os
from datetime import datetime

from github import Auth
from github import Github
from telegram.ext import Application

logger = logging.getLogger(__name__)


class GitHubIssuePoller:
    chats = []

    def __init__(self, application: Application):
        with open("chats.txt") as f:
            for line in f.readlines():
                self.chats.append(int(line))
        self.running = True
        self.issues = None
        token = os.environ['GH_TOKEN']
        self.auth = Auth.Token(token)
        self.g = Github(auth=self.auth)
        self.repo = self.g.get_repo(os.environ['GH_REPO'])
        self.application = application
        self.current_issues = {}

    async def poll_issues(self):
        while self.running:
            logger.info("Polling issues")
            try:
                self.issues = self.repo.get_issues(state='open', labels=["status"])
                if self.issues.totalCount < len(self.current_issues):
                    await self._send_message_host_is_up()
                if len(self.chats) > 0:
                    for chat_id in self.chats:
                        await self._process_issues(chat_id)
                logger.info("Got issues: " + str(self.issues.totalCount))
            except Exception as e:
                logger.error("Exception: " + str(type(e)) + " " + str(e))
            await asyncio.sleep(30)

    async def _process_issues(self, chat_id):
        for issue in self.issues:
            if issue.id not in self.current_issues.keys():
                self.current_issues[issue.id] = {}
                self.current_issues[issue.id]["time"] = datetime.now()
                self.current_issues[issue.id]["issue"] = issue
                message = self._issue_to_message(issue)

                await self._send_message_to_chat(chat_id, message)

            else:
                if diff_minutes_round(datetime.now(), self.current_issues[issue.id]["time"]) > 15:
                    self.current_issues[issue.id]["time"] = datetime.now()
                    message = self._issue_to_message(issue)
                    message = message.replace("is", "is still")

                    await self._send_message_to_chat(chat_id, message)

    @staticmethod
    def _issue_to_message(issue) -> str:
        message = issue.title
        return message

    async def _send_message_to_chat(self, chat_id, message):
        await self.application.bot.send_message(chat_id, message,
                                                parse_mode="Markdown",
                                                disable_web_page_preview=True)
        await asyncio.sleep(1)

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

    async def _send_message_host_is_up(self):
        issue_ids_from_api = []
        for issue in self.issues:
            issue_ids_from_api.append(issue.id)

        issue_ids_to_remove = []
        for issue_id in self.current_issues.keys():
            if issue_id not in issue_ids_from_api:
                message = self._issue_to_message(self.current_issues[issue_id]["issue"])
                message = message.replace("🛑", "🟢")
                message = message.replace("down", "up")

                for chat_id in self.chats:
                    await self._send_message_to_chat(chat_id, message)
                    await asyncio.sleep(1)

                issue_ids_to_remove.append(issue_id)

        for issue_id in issue_ids_to_remove:
            self.current_issues.pop(issue_id)


def diff_minutes_round(date1: datetime, date2: datetime) -> int:
    diff = (date1 - date2).seconds / 60
    return abs(round(diff))
