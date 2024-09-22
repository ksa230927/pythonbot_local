from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import html, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db.execute import execute_query
from bot.db.connection import connection

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    timestamp_now = datetime.now(tz=ZoneInfo("UTC")).isoformat(sep=" ")
    insert_query = f"""
    INSERT INTO message (description, user_id, m_timestamp)
    VALUES ('{message.text}', {message.from_user.id}, 'message_timestamp');
    """
    execute_query(connection, insert_query)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        timestamp_now = datetime.now(tz=ZoneInfo("UTC")).isoformat(sep=" ")
        insert_query = f"""
            INSERT INTO posts (description, user_id, m_timestamp)
            VALUES ('{message.text}', {message.from_user.id}, 'message_timestamp');
            """
        execute_query(connection, insert_query)
        # Send a copy of the received message

        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!code")
