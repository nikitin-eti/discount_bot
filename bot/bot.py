import logging
import ssl
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import aiocron

from config import CONFIG, TOKEN, WEBHOOK_SECRET
from handlers import setup_handlers
from middlewares import log_request
from webhook import on_startup
from tasks import send_weekly_updates
from data_management.update_database import main as create_db

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger(__name__)


def main():
    """ Main function """
    dp = Dispatcher()
    bot = Bot(token=TOKEN)

    create_db()

    setup_handlers(dp)

    dp.startup.register(on_startup)

    app = web.Application(middlewares=[log_request])
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET)
    handler.register(app, path=CONFIG["WEBHOOK_PATH"])
    setup_application(app, dp, bot=bot)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(CONFIG["WEBHOOK_SSL_CERT"], CONFIG["WEBHOOK_SSL_PRIV"])

    # Schedule the weekly updates every Friday at 12:00 PM
    aiocron.crontab('0 12 * * FRI', func=send_weekly_updates, args=(bot,))

    logger.info("Запуск веб-сервера...")
    web.run_app(app, host=CONFIG["WEB_SERVER_HOST"], port=CONFIG["WEB_SERVER_PORT"], ssl_context=context)


if __name__ == "__main__":
    logger.info("Запуск бота...")
    main()