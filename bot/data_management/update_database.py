import logging

import feedparser
import sqlite3
from sqlite3 import Error
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'free_games.db')
logger = logging.getLogger(__name__)


def get_all_free_games(conn):
    """
    Parses new games from the RSS feed and formats them into a compact-looking message

    Args:
        conn: Connection object

    Returns:
        a dictionary containing the current's free game link + description
    """
    url = "https://www.indiegamebundles.com/category/free/rss"
    free_game_dict = dict()
    conn.execute("DELETE FROM free_games")
    conn.commit()

    try:
        d = feedparser.parse(url)
        for entry in d.entries:
            free_description = entry.title
            free_link = entry.link
            if free_link not in free_game_dict:
                insert_free_game(conn, (free_link, free_description))
                free_game_dict[free_link] = free_description
    except Exception as e:
        logging.info(f"The site is currently down or unreachable:\t{e}")

    return free_game_dict


def create_connection(db_file):
    """
    Create a database connection to a SQLite database

    Args:
        db_file: database file

    Returns:
        a Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info(f"Connected to {db_file}")
    except Error as e:
        logging.info(f"Error connecting to {db_file}:\t{e}")
    return conn


def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement

    Args:
        conn: Connection object
        create_table_sql: a CREATE TABLE statement

    Returns:
        None
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        logging.info("Table created")
    except Error as e:
        logging.info(f"Error creating table:\t{e}")


def insert_free_game(conn, free_game):
    """
    Insert a new free game into the free_games table

    Args:
        conn: Connection object
        free_game: a tuple containing the free game's link and description

    Returns:
        None
    """
    sql = """
        INSERT OR IGNORE INTO free_games (url, name)
        VALUES (?, ?)
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, free_game)
        conn.commit()
    except Error as e:
        logging.info(f"Error inserting free game:\t{e}")


def insert_user(conn, user):
    """
    Insert a new user into the users_chats table

    Args:
        conn: Connection object
        user: a tuple containing the user ID and group ID

    Returns:
        None
    """
    sql = """
        INSERT OR IGNORE INTO users_chats (user_id, group_id)
        VALUES (?, ?)
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()

        users = get_all_users(conn)
        last_5_users = users[-5:]
        logging.info(f"Last 5 users: {last_5_users}")

    except Error as e:
        logging.info(f"Error inserting user:\t{e}")


def main():
    database_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db')
    database = DATABASE_PATH

    if not os.path.exists(database_dir):
        os.makedirs(database_dir)

    sql_create_free_games_table = """
    CREATE TABLE IF NOT EXISTS free_games (
        url TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """

    sql_create_users_chats_table = """
    CREATE TABLE IF NOT EXISTS users_chats (
        user_id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL
    )
    """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_free_games_table)
        create_table(conn, sql_create_users_chats_table)
        free_games = get_all_free_games(conn)
        logging.info(free_games)
    else:
        logging.info("Error! Cannot create the database connection.")


def get_all_users(conn):
    """
    Получить список всех пользователей из базы данных.

    Args:
        conn: Connection object

    Returns:
        список всех user_id и group_id
    """
    sql = "SELECT user_id, group_id FROM users_chats"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        users = cur.fetchall()
        return users
    except Error as e:
        logging.info(f"Error fetching users:\t{e}")
        return []


if __name__ == '__main__':
    main()
