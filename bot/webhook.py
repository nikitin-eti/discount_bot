from aiogram import Bot
from aiogram.types import FSInputFile
from config import CONFIG, WEBHOOK_SECRET
import logging

logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    logger.info("Устанавливаем вебхук для бота...")
    await bot.set_webhook(
        f"{CONFIG['BASE_WEBHOOK_URL']}{CONFIG['WEBHOOK_PATH']}",
        certificate=FSInputFile(CONFIG["WEBHOOK_SSL_CERT"]),
        secret_token=WEBHOOK_SECRET,
    )
    logger.info(f"Вебхук установлен: {CONFIG['BASE_WEBHOOK_URL']}{CONFIG['WEBHOOK_PATH']}")
