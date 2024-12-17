import os
import sys
import logging
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, User

from exceptions import MovieAPIError, MovieNotFound, UndefinedUser
from msg_constructors import construct_history_message, construct_stat_message, \
    construct_message, start_msg, help_msg
from db_manipulations import write_entry, fetch_history, fetch_stats
from fetchers import get_kinopoisk_info, get_film_info


BOT_TOKEN = os.getenv("TOKEN")
db_connection = sqlite3.connect('db/cinemabot.db', autocommit=True)
dp = Dispatcher()


@dp.message(Command(commands='history'))
async def command_history_handler(message: Message) -> None:
    try:
        data = fetch_history(db_connection, message.from_user)
        await message.answer(construct_history_message(data))
    except UndefinedUser:
        await message.answer('Unable to define your user_id')


@dp.message(Command(commands='stats'))
async def command_stats_handler(message: Message) -> None:
    try:
        data = fetch_stats(db_connection, message.from_user)
        await message.answer(construct_stat_message(data))
    except UndefinedUser:
        await message.answer('Unable to define your user_id')


@dp.message(Command(commands='start'))
async def command_start_handler(message: Message) -> None:
    await message.answer(start_msg)


@dp.message(Command(commands='help'))
async def command_help_handler(message: Message) -> None:
    await message.answer(help_msg)


@dp.message()
async def query_handler(message: Message) -> None:
    try:
        sender: User | None = message.from_user
        query: str | None = message.text

        if query is None:
            raise TypeError

        kp_id, *pirate_urls = await get_kinopoisk_info(query)
        name, desc, rating, votes, poster, year = await get_film_info(kp_id)
        write_entry(db_connection, sender, ("%s (%s)") % (name, year if year != '' else '?'), query)

        caption = construct_message(pirate_urls,
                                    name,
                                    desc,
                                    rating,
                                    votes,
                                    year)

        if poster != "":
            await message.answer_photo(poster, caption)
        else:
            await message.answer(caption)
    except MovieNotFound:
        await message.answer("Movie not found, try to resend query with more information")
    except MovieAPIError:
        await message.answer("Something is wrong with API we're using, try again next time")
    except TypeError:
        await message.answer("Such query is not supported, please use /help")
    except Exception:
        await message.answer("Unpredicted error occured")


async def main() -> None:
    assert BOT_TOKEN is not None
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    db_connection.close()
