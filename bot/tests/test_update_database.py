import os
import pytest
from unittest.mock import patch, MagicMock
from bot.data_management.update_database import create_connection, create_table, insert_user, get_all_users, \
    insert_free_game, get_all_free_games


@pytest.fixture
def setup_database():
    test_db = 'test_free_games.db'
    conn = create_connection(test_db)
    yield conn
    conn.close()
    os.remove(test_db)


def test_create_connection(setup_database):
    conn = setup_database
    assert conn is not None


def test_create_table(setup_database):
    conn = setup_database
    sql_create_users_chats_table = """
    CREATE TABLE IF NOT EXISTS users_chats (
        user_id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL
    )
    """
    create_table(conn, sql_create_users_chats_table)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_chats'")
    table = cur.fetchone()
    assert table is not None


def test_insert_user(setup_database):
    conn = setup_database
    sql_create_users_chats_table = """
    CREATE TABLE IF NOT EXISTS users_chats (
        user_id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL
    )
    """
    create_table(conn, sql_create_users_chats_table)
    insert_user(conn, (1, 1))
    users = get_all_users(conn)
    assert len(users) == 1
    assert users[0] == (1, 1)


def test_insert_free_game(setup_database):
    conn = setup_database
    sql_create_free_games_table = """
    CREATE TABLE IF NOT EXISTS free_games (
        url TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """
    create_table(conn, sql_create_free_games_table)
    insert_free_game(conn, ('http://example.com', 'Example Game'))
    cur = conn.cursor()
    cur.execute("SELECT * FROM free_games")
    games = cur.fetchall()
    assert len(games) == 1
    assert games[0] == ('http://example.com', 'Example Game')


@patch('bot.data_management.update_database.feedparser.parse')
def test_get_all_free_games(mock_feedparser, setup_database):
    conn = setup_database
    sql_create_free_games_table = """
    CREATE TABLE IF NOT EXISTS free_games (
        url TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """
    create_table(conn, sql_create_free_games_table)
    insert_free_game(conn, ('http://example.com', 'Example Game'))

    mock_feed = MagicMock()

    entry = MagicMock()
    entry.title = 'Example Game'
    entry.link = 'http://example.com'

    mock_feed.entries = [entry]

    mock_feedparser.return_value = mock_feed

    free_games = get_all_free_games(conn)

    assert 'http://example.com' in free_games
    assert free_games['http://example.com'] == 'Example Game'