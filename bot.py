import asyncio
import logging
import os

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ContextTypes, ApplicationBuilder

from github_poller import GitHubIssuePoller
from pinger import SitePinger

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    logger.info("Adding chat to the list: " + str(chat_id))
    GitHubIssuePoller.add_chat(chat_id)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    tg_token = os.environ["TG_TOKEN"]

    application = ApplicationBuilder().token(tg_token).build()

    pinger = SitePinger(application)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    asyncio.get_event_loop().create_task(pinger.ping_sites())
    asyncio.get_event_loop().create_task(pinger.check_sites_and_send_message())

    application.run_polling()


if __name__ == '__main__':
    main()
