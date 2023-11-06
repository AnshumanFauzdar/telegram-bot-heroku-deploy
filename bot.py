import asyncio
import logging
import os

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ContextTypes, ApplicationBuilder

from github_poller import GitHubIssuePoller

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    tg_token = os.environ["TG_TOKEN"]

    application = ApplicationBuilder().token(tg_token).build()

    github_issues = GitHubIssuePoller()

    loop = asyncio.get_event_loop()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    github_issues.get_issues()
    application.run_polling()


if __name__ == '__main__':
    main()
