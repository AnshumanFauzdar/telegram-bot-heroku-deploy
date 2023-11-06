import asyncio
from multiprocessing import get_logger
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncContextManager,
    Callable,
    Coroutine,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from github import Github
from github import Auth
import os

_LOGGER = get_logger()


class GitHubIssuePoller:
    def __init__(self):
        self.running = True
        self.issues = None
        token = os.environ['GH_TOKEN']
        self.auth = Auth.Token(token)
        self.g = Github(auth=self.auth)
        self.repo = g.get_repo('boriskhodok/wowsuptime')

    def get_issues(self):
        asyncio.run(self.poll_issues())

    async def poll_issues(self):
        while self.running:
            print("Polling issues")
            self.issues = self.g.get_issues(state='open')

            print("Got issues: " + str(self.issues.totalCount))
            await asyncio.sleep(30)

    async def shutdown(self) -> None:
        if self.running:
            raise RuntimeError("This Poller is still running!")

        self.running = False
        _LOGGER.debug("Shut down of Poller complete")
