import sqlite3
from exceptions import UndefinedUser
from aiogram.types import User


def write_entry(connection: sqlite3.Connection, sender: User | None, film_name: str, query) -> None:
    if sender is None:
        return
    cursor = connection.cursor()
    user_id = sender.id
    try:
        cursor.execute("""
        INSERT INTO history (user_id, query, film)
        VALUES(?, ?, ?)
        """, (user_id, query, film_name))
    except Exception:
        pass
    finally:
        cursor.close()


def fetch_history(connection: sqlite3.Connection, sender: User | None) -> list[tuple[str, str]]:
    db_cursor = connection.cursor()
    try:
        if sender is None:
            raise UndefinedUser
        data = db_cursor.execute("""SELECT query, film FROM History
                                    WHERE user_id = :user_id
                                    ORDER BY id DESC""", {"user_id": sender.id}).fetchall()
        return data
    finally:
        db_cursor.close()


def fetch_stats(connection: sqlite3.Connection, sender: User | None) -> list[tuple[str, int]]:
    db_cursor = connection.cursor()
    try:
        if sender is None:
            raise UndefinedUser
        data = db_cursor.execute("""SELECT film, COUNT(film) as occs
                                    FROM History
                                    WHERE user_id = :user_id
                                    GROUP BY film
                                    ORDER BY occs DESC""", {"user_id": sender.id}).fetchall()
        return data
    finally:
        db_cursor.close()
