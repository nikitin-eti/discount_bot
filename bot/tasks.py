import logging
from aiogram import Bot
from data_management.update_database import create_connection, get_all_free_games, DATABASE_PATH, get_all_users

logger = logging.getLogger(__name__)

async def send_weekly_updates(bot: Bot):
    conn = create_connection(DATABASE_PATH)
    if conn:
        users = get_all_users(conn)
        free_games = get_all_free_games(conn)
        conn.close()

        if free_games:
            games_message = "Вот список новых бесплатных игр:\n\n"
            for url, description in free_games.items():
                games_message += f"{description}\n{url}\n\n"
        else:
            games_message = "К сожалению, нет новых бесплатных игр на данный момент."

        for user_id, group_id in users:
            try:
                await bot.send_message(group_id, games_message)
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
    else:
        logger.error("Ошибка при создании соединения с базой данных")