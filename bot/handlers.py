from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from data_management.update_database import create_connection, insert_user, get_all_free_games, DATABASE_PATH
import logging
from tasks import send_weekly_updates

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command('start'))
async def command_start_handler(message: Message):
    """Обработчик команды /start"""
    logger.info(f"Получено сообщение от {message.from_user.full_name}: /start")
    user_id = message.from_user.id
    group_id = message.chat.id

    conn = create_connection(DATABASE_PATH)
    if conn:
        insert_user(conn, (user_id, group_id))
        conn.close()
        logger.info(f"Пользователь {message.from_user.full_name} добавлен в базу данных")
    else:
        logger.error("Ошибка при создании соединения с базой данных")

    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}! Вы были добавлены в базу данных для получения еженедельных обновлений.")


@router.message(Command('admin_test'))
async def command_admin_test_handler(message: Message):
    """Обработчик команды /admin_test для отправки еженедельных обновлений всем пользователям"""
    await send_weekly_updates(message.bot)


@router.message(Command('new'))
async def command_new_handler(message: Message):
    """Обработчик команды /new для получения списка новых бесплатных игр"""
    logger.info(f"Получено сообщение от {message.from_user.full_name}: /new")

    conn = create_connection(DATABASE_PATH)
    if conn:
        free_games = get_all_free_games(conn)
        conn.close()

        if free_games:
            games_message = "Вот список новых бесплатных игр:\n\n"
            for url, description in free_games.items():
                games_message += f"{description}\n{url}\n\n"
        else:
            games_message = "К сожалению, нет новых бесплатных игр на данный момент."
    else:
        games_message = "Произошла ошибка при подключении к базе данных."

    await message.answer(games_message)


def setup_handlers(dp):
    """Install all handlers"""
    dp.include_router(router)
