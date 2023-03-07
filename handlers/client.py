import asyncio
import logging
import sqlite3

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery
from aiogram.utils import markdown as md

from create_bot import bot, Chat_id
from keyboards import kb_menu, kb_client, url_con, url_coursс


class Form(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Cons = State()


conn = sqlite3.connect('db.db')


def registere_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        command_start,
        Text(equals=['/start', '/help', 'start', 'старт'],
             ignore_case=True)
    )
    dp.register_message_handler(
        menu,
        lambda message: 'Вернуться в меню' in message.text,
        state=None
    )
    dp.register_message_handler(
        zayavka,
        lambda message: 'Подать заявку' in message.text,
        state=None
    )
    dp.register_message_handler(
        cancel_handler1,
        Text(equals=['/start', '/help', 'start', 'старт', 'Вернуться в меню'],
             ignore_case=True),
        state='*'
    )
    dp.register_message_handler(
        answer_q1,
        state=Form.Q1
    )
    dp.register_message_handler(
        cancel_handler2,
        Text(equals=['/start', '/help', 'start', 'старт', 'Вернуться в меню'],
             ignore_case=True),
        state='*'
    )
    dp.register_message_handler(
        answer_q2,
        state=Form.Q2
    )
    dp.register_message_handler(
        cancel_handler3,
        Text(equals=['/start', '/help', 'start', 'старт', 'Вернуться в меню'],
             ignore_case=True),
        state='*'
    )
    dp.register_message_handler(
        answer_q3,
        state=Form.Q3
    )
    dp.register_message_handler(
        con,
        lambda message: 'Контакты' in message.text,
        state=None
    )
    dp.register_message_handler(
        disk,
        lambda message: 'Узнать о скидках' in message.text,
        state=None
    )
    dp.register_message_handler(
        coursesc,
        lambda message: 'Узнать о курсах в студии' in message.text,
        state=None
    )
    dp.register_callback_query_handler(
        coursesc_call,
        Text(equals=['Впередк', 'Назадк', 'Подать заявку']),
        state=None
    )


async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Здравствуйте, я бот помощник')
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE userid = ?', (user_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT INTO users (userid, blacklist) VALUES (?, ?)',
                       (user_id, 0)
                       )
        conn.commit()
    await asyncio.sleep(1)
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_client
    )


async def block_check(user_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT blacklist FROM users WHERE userid = ?", (user_id,))
    result = cursor.fetchone()
    if result is not None:
        if result[0] == 1:
            await types.ChatActions.typing(1)
            await bot.send_message(
                chat_id=user_id,
                text="Вы заблокированы и не можете отправлять заявки."
            )
            await asyncio.sleep(1)
            await bot.send_message(
                chat_id=user_id,
                text="Выберите пункт меню:",
                reply_markup=kb_client
            )
            return True
        else:
            return False
    else:
        return False


async def coursesc(message: types.Message):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM courses")
    count_cours = cursor.fetchone()[0]
    current_page = 1
    cursor.execute(f"SELECT * FROM courses LIMIT 1 OFFSET {current_page - 1}")
    cours = cursor.fetchone()[1:]
    await bot.send_message(
        message.from_user.id,
        f"{cours[1]}\n\nНомер данного курса: {current_page}\n"
        f"Всего курсов: {count_cours}\n\n{current_page}/{count_cours}",
        reply_markup=url_coursс
    )


async def coursesc_call(callback: CallbackQuery, state: FSMContext):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM courses")
    PAGE_COUNT = cursor.fetchone()[0]
    current_page = int(callback.message.text.split('\n')[-1].split('/')[0])

    if callback.data == 'Впередк':
        if int(current_page) < PAGE_COUNT:
            current_page = str(int(current_page) + 1)
            cursor.execute(
                f"SELECT * FROM courses LIMIT 1 OFFSET {int(current_page) - 1}"
            )
            cours = cursor.fetchone()[1:]
            await callback.message.edit_text(
                f"{cours[1]}\n\nНомер данного курса: {current_page}\n"
                f"Всего курсов: {PAGE_COUNT}\n\n{current_page}/{PAGE_COUNT}",
                reply_markup=url_coursс
            )

    elif callback.data == 'Назадк':
        if int(current_page) > 1:
            current_page = str(int(current_page) - 1)
            cursor.execute(
                f"SELECT * FROM courses LIMIT 1 OFFSET {int(current_page) - 1}"
            )
            cours = cursor.fetchone()[1:]
            await callback.message.edit_text(
                f"{cours[1]}\n\nНомер данного курса: {current_page}\n"
                f"Всего курсов: {PAGE_COUNT}\n\n{current_page}/{PAGE_COUNT}",
                reply_markup=url_coursс
            )

    elif callback.data == 'Подать заявку':
        if await block_check(callback.from_user.id):
            return
        await callback.message.answer(
            'Здравствуте, что бы подать заявку, заполните анкету:',
            reply_markup=kb_menu
        )
        await asyncio.sleep(1)
        await callback.message.answer(
            'Укажите ваше Имя:',
            reply_markup=kb_menu
        )
        await Form.Q1.set()


async def zayavka(message: types.Message):
    if await block_check(message.from_user.id):
        return
    await bot.send_message(
        message.from_user.id,
        'Здравствуте, что бы подать заявку, заполните анкету:',
        reply_markup=kb_menu
    )
    await asyncio.sleep(1)
    await bot.send_message(
        message.from_user.id,
        'Укажите ваше Имя:',
        reply_markup=kb_menu
    )
    await Form.Q1.set()


async def cancel_handler1(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_client
    )


async def answer_q1(message: types.Message, state: FSMContext):
    answer1 = message.text
    async with state.proxy() as data:
        data["answer1"] = answer1
    await bot.send_message(
        message.from_user.id,
        'Укажите возраст:',
        reply_markup=kb_menu
    )
    await Form.Q2.set()


async def cancel_handler2(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_client
    )


async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    async with state.proxy() as data:
        data["answer2"] = answer2
    await bot.send_message(
        message.from_user.id,
        'Укажите ваш конактный номер:',
        reply_markup=kb_menu
    )
    await Form.Q3.set()


async def cancel_handler3(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_client
    )


async def answer_q3(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    answer3 = message.text
    async with state.proxy() as data:
        data["answer3"] = answer3
    await bot.send_message(
        Chat_id,
        md.text(
            md.bold(f'Новая заявка от пользователя {user_id}:'),
            ' ',
            md.bold('Имя: ') + (data['answer1']),
            md.bold('Возраст: ') + (data['answer2']),
            md.bold('Номер телефона: ') + (data['answer3']),
            sep='\n'
        ),
        parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(
        message.from_user.id,
        'Спасибо! Мы получили вашу анкету и обязательно вам перезвоним.',
        reply_markup=kb_menu
    )
    await state.finish()
    await asyncio.sleep(1)
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_client
    )


async def con(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        ('''Наши контакты и соц.сети:

🔹 Телефон: +79999999999

🔹 Мы находимся тут: г. Москва проспект, пр. Петрова 3'''),
        reply_markup=url_con)


async def disk(message: types.Message):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM discounts WHERE id = 1')
    result = cursor.fetchone()
    await bot.send_message(
        message.from_user.id,
        f'{result[1]}',
        reply_markup=kb_menu
    )


async def menu(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_client
    )
