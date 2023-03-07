import asyncio

from aiogram import types, Dispatcher

from create_bot import bot
from keyboards import kb_client


def registere_handlers_other(dp: Dispatcher):
    dp.register_message_handler(empty)


async def empty(message: types.Message):
    await message.answer(
        'Сообщение не распознано - такой команды не существует.'
    )
    await asyncio.sleep(1)
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_client
    )
