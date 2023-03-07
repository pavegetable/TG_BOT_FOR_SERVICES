import asyncio
import logging
import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from create_bot import Dispatcher, bot
from keyboards import (
    kb_admin, kb_adminback, kb_client, kb_clients,
    url_cours, url_spam, url_spamf
)

# ID модераторов и их имена
# ID пользователя можно узнать с помощью бота getmyid_bot
moderators_ID = {
    245352523452451: 'Павел',
    56422151354325: 'Ксения'
}


conn = sqlite3.connect('db.db')


class Form(StatesGroup):
    text = State()
    photo = State()
    Statee = State()
    ban = State()
    unban = State()
    status = State()
    disk = State()
    add = State()
    edit = State()


def registere_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        adminstart,
        commands=['moderator'],
        state=None
    )
    dp.register_message_handler(
        adminback,
        lambda message: 'Вернуться в админ-меню' in message.text,
        state=None
    )
    dp.register_message_handler(
        adminleave,
        lambda message: 'Выйти из Админ-Панели' in message.text,
        state=None
    )
    dp.register_message_handler(
        adminspam,
        lambda message: 'Создать рассылку' in message.text,
        state=None
    )
    dp.register_message_handler(
        cancel_handlerspam,
        lambda message: 'Вернуться в админ-меню' in message.text,
        state='*'
    )
    dp.register_message_handler(
        halfspam,
        state=Form.text
    )
    dp.register_callback_query_handler(
        send_text,
        text='next',
        state=Form.Statee
    )
    dp.register_callback_query_handler(
        add_photo,
        text='add_photo',
        state=Form.Statee
    )
    dp.register_message_handler(
        spam_text,
        state=Form.photo,
        content_types=types.ContentType.PHOTO
    )
    dp.register_callback_query_handler(
        send_text_ag,
        text='next',
        state=Form.photo
    )
    dp.register_callback_query_handler(
        quit,
        text='otmena',
        state='*'
    )
    dp.register_message_handler(
        adminban,
        lambda message: 'Заблокировать пользователя' in message.text,
        state=None
    )
    dp.register_message_handler(
        cancel_handlerban,
        lambda message: 'Вернуться в админ-меню' in message.text,
        state='*'
    )
    dp.register_message_handler(
        finalban,
        state=Form.ban
    )
    dp.register_message_handler(
        adminunban,
        lambda message: 'Разблокировать пользователя' in message.text,
        state=None
    )
    dp.register_message_handler(
        cancel_handlerunban,
        lambda message: 'Вернуться в админ-меню' in message.text,
        state='*'
    )
    dp.register_message_handler(
        finalunban,
        state=Form.unban
    )
    dp.register_message_handler(
        adminusers,
        lambda message: 'Управление пользователями' in message.text,
        state=None
    )
    dp.register_message_handler(
        adminstatus,
        lambda message: 'Статус пользователя' in message.text,
        state=None
    )
    dp.register_message_handler(
        cancel_handlerstatus,
        lambda message: 'Вернуться в админ-меню' in message.text,
        state='*'
    )
    dp.register_message_handler(
        finalstatus,
        state=Form.status
    )
    dp.register_message_handler(
        stat,
        lambda message: 'Статистика' in message.text,
        state=None
    )
    dp.register_message_handler(
        admindisc,
        lambda message: 'Изменить информацию о скидках' in message.text,
        state=None
    )
    dp.register_message_handler(
        cancel_handlerdisc,
        lambda message: 'Вернуться в админ-меню' in message.text,
        state='*'
    )
    dp.register_message_handler(
        finaldisc,
        state=Form.disk
    )
    dp.register_message_handler(
        courses,
        lambda message: 'Изменить информацию о курсах' in message.text,
        state=None
    )
    dp.register_callback_query_handler(
        courses_call,
        Text(equals=['Вперед', 'Назад', 'Редактировать', 'Удалить',
                     'Добавить']),
        state=None
    )
    dp.register_message_handler(
        cancel_handleradd,
        lambda message: 'Вернуться в админ-меню' in message.text,
        state='*'
    )
    dp.register_message_handler(
        finaladd,
        state=Form.add
    )
    dp.register_message_handler(
        finaledit,
        state=Form.edit
    )


async def adminstart(message: types.Message):
    if message.from_user.id in moderators_ID:
        name = moderators_ID[message.from_user.id]
        await bot.send_message(
            message.from_user.id,
            f'Добро пожаловать в Админ-Панель, {name}! Выберите пункт меню:',
            reply_markup=kb_admin
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def adminback(message: types.Message):
    if message.from_user.id in moderators_ID:
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_admin
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def adminleave(message: types.Message):
    if message.from_user.id in moderators_ID:
        name = moderators_ID[message.from_user.id]
        await bot.send_message(
            message.from_user.id,
            f"{name}, вы вышли из Админ-Панели. "
            f"Чтобы снова попасть в Админ-Панель, напишите /moderator"
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            "Выберите пункт меню:",
            reply_markup=kb_client
        )
    else:
        await bot.send_message(
            message.from_user.id,
            "У вас недостаточно прав"
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            "Выберите пункт меню:",
            reply_markup=kb_client
        )


async def adminspam(message: types.Message):
    if message.from_user.id in moderators_ID:
        await bot.send_message(
            message.from_user.id,
            'Укажите текст, который разослать пользователям:',
            reply_markup=kb_adminback
        )
        await bot.send_message(
            message.from_user.id,
            'Если хотите вернуться в меню, нажмите "Вернуться в админ-меню"',
            reply_markup=kb_adminback
        )
        await Form.text.set()
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def cancel_handlerspam(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def halfspam(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=url_spam)
    await Form.Statee.set()


async def send_text(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    await state.finish()

    cursor = conn.cursor()
    cursor.execute('SELECT userid FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    for user_id in user_ids:
        Chat_id = user_id
        await bot.send_message(Chat_id, text=text)
    await call.message.answer(
        f"Рассылка отправлена.\n"
        f"Количество пользователей, которые получили рассылку: {total_users}"
    )

    await state.finish()

    await asyncio.sleep(1)
    await call.message.answer(
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Прикрепите фото:')
    await Form.photo.set()


async def spam_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=url_spamf
    )


async def send_text_ag(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()

    cursor = conn.cursor()
    cursor.execute('SELECT userid FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    for user_id in user_ids:
        Chat_id = user_id
        await bot.send_photo(Chat_id, photo=photo, caption=text)
    await call.message.answer(
        f"Рассылка отправлена.\n"
        f"Количество пользователей, которые получили рассылку: {total_users}"
    )

    await state.finish()

    await asyncio.sleep(1)
    await call.message.answer(
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def quit(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Рассылка отменена')
    await asyncio.sleep(1)
    await call.message.answer(
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def adminban(message: types.Message):
    if message.from_user.id in moderators_ID:
        await bot.send_message(
            message.from_user.id,
            'Укажите ID пользователя, которого хотите заблокировать:',
            reply_markup=kb_adminback
        )
        await Form.ban.set()
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def cancel_handlerban(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def finalban(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ban'] = str(message.text)

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE userid = '{data['ban']}'")
    result = cursor.fetchone()

    if result:
        blacklist = result[2]
        if blacklist == 1:
            await bot.send_message(
                message.from_user.id,
                f"Пользователь {data['ban']} уже заблокирован",
                reply_markup=kb_clients
            )
        else:
            cursor.execute(
                f"UPDATE users SET blacklist = 1 "
                f"WHERE userid = '{data['ban']}'"
            )
            conn.commit()

            await bot.send_message(
                message.from_user.id,
                f"Пользователь {data['ban']} заблокирован",
                reply_markup=kb_clients
            )
    else:
        await bot.send_message(
            message.from_user.id,
            f"Пользователя {data['ban']} нет в базе данных, проверьте ID и "
            f"попробуйте снова, нажав в меню на «Заблокировать пользователя»",
            reply_markup=kb_clients
        )
    await state.finish()


async def adminunban(message: types.Message):
    if message.from_user.id in moderators_ID:
        await bot.send_message(
            message.from_user.id,
            'Укажите ID пользователя, которого хотите разблокировать:',
            reply_markup=kb_adminback
        )
        await Form.unban.set()
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def cancel_handlerunban(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def finalunban(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['unban'] = str(message.text)

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE userid = '{data['unban']}'")
    result = cursor.fetchone()

    if result:
        blacklist = result[2]
        if blacklist == 0:
            await bot.send_message(
                message.from_user.id,
                f"Пользователь {data['unban']} не заблокирован",
                reply_markup=kb_clients
            )
        else:
            cursor.execute(
                f"UPDATE users SET blacklist = 0 "
                f"WHERE userid = '{data['ban']}'"
            )
            conn.commit()

            await bot.send_message(
                message.from_user.id,
                f"Пользователь {data['unban']} разблокирован",
                reply_markup=kb_clients
            )
    else:
        await bot.send_message(
            message.from_user.id,
            f"Пользователя {data['unban']} нет в базе данных, проверьте ID и "
            f"попробуйте снова, нажав в меню на «Разблокировать пользователя»",
            reply_markup=kb_clients
        )
    await state.finish()


async def adminusers(message: types.Message):
    if message.from_user.id in moderators_ID:
        await bot.send_message(
            message.from_user.id,
            'Вы вошли в раздел управления пользователями. Выберите действие:',
            reply_markup=kb_clients
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def adminstatus(message: types.Message):
    if message.from_user.id in moderators_ID:
        await bot.send_message(
            message.from_user.id,
            'Укажите ID пользователя, статус которого вы хотите узнать:',
            reply_markup=kb_adminback
        )
        await Form.status.set()
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def cancel_handlerstatus(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def finalstatus(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['status'] = str(message.text)

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE userid = '{data['status']}'")
    result = cursor.fetchone()

    if result:
        blacklist = result[2]
        if blacklist == 0:
            await bot.send_message(
                message.from_user.id,
                f"Пользователь {data['status']} не заблокирован",
                reply_markup=kb_clients
            )
        else:
            await bot.send_message(
                message.from_user.id,
                f"Пользователь {data['status']} заблокирован",
                reply_markup=kb_client
            )
    else:
        await bot.send_message(
            message.from_user.id,
            f"Пользователя {data['status']} нет в базе данных, проверьте ID и "
            f"попробуйте снова, нажав в меню на «Статус пользователя»",
            reply_markup=kb_clients
        )
    await state.finish()


async def stat(message: types.Message):
    if message.from_user.id in moderators_ID:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users WHERE blacklist = 1")
        banned_users = cursor.fetchone()[0]

        await bot.send_message(
            message.from_user.id,
            f"Количество пользователей бота: {total_users}\n"
            f"Количество заблокированных пользователей: {banned_users}",
            reply_markup=kb_clients
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def admindisc(message: types.Message):
    if message.from_user.id in moderators_ID:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM discounts WHERE id = 1')
        result = cursor.fetchone()

        await bot.send_message(
            message.from_user.id,
            f'{result[1]}',
            reply_markup=kb_adminback
        )
        await bot.send_message(
            message.from_user.id,
            "Если хотите отредактировать, введите новый текст. "
            "В ином случае нажминате в меню «Вернуться в админ-меню»",
            reply_markup=kb_adminback
        )
        await Form.disk.set()
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def cancel_handlerdisc(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def finaldisc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['disk'] = str(message.text)

    cursor = conn.cursor()
    cursor.execute(
        'UPDATE discounts SET discounts = ? WHERE id = 1',
        (data['disk'],)
    )
    conn.commit()

    await bot.send_message(
        message.from_user.id,
        'Данные по скидкам обновлены',
        reply_markup=kb_admin
    )
    await state.finish()

    await asyncio.sleep(1)
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def courses(message: types.Message):
    if message.from_user.id in moderators_ID:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses")
        count_cours = cursor.fetchone()[0]

        current_page = 1
        cursor.execute(
            f"SELECT * FROM courses LIMIT 1 OFFSET {current_page - 1}"
        )
        cours = cursor.fetchone()[1:]

        await bot.send_message(
            message.from_user.id,
            f"{cours[1]}\n\nНомер данного курса: {current_page}\n"
            f"Всего курсов: {count_cours}\n\n{current_page}/{count_cours}",
            reply_markup=url_cours
        )
    else:
        await bot.send_message(
            message.from_user.id,
            'У вас недостаточно прав'
        )
        await asyncio.sleep(1)
        await bot.send_message(
            message.from_user.id,
            'Выберите пункт меню:',
            reply_markup=kb_client
        )


async def courses_call(callback: CallbackQuery, state: FSMContext):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM courses')
    PAGE_COUNT = cursor.fetchone()[0]
    current_page = int(callback.message.text.split('\n')[-1].split('/')[0])

    if callback.data == 'Вперед':
        if int(current_page) < PAGE_COUNT:
            current_page = str(int(current_page) + 1)
            cursor.execute(
                f"SELECT * FROM courses LIMIT 1 OFFSET {int(current_page) - 1}"
            )
            cours = cursor.fetchone()[1:]

            await callback.message.edit_text(
                f"{cours[1]}\n\nНомер данного курса: {current_page}\n"
                f"Всего курсов: {PAGE_COUNT}\n\n{current_page}/{PAGE_COUNT}",
                reply_markup=url_cours
            )

    elif callback.data == 'Назад':
        if int(current_page) > 1:
            current_page = str(int(current_page) - 1)
            cursor.execute(
                f"SELECT * FROM courses LIMIT 1 OFFSET {int(current_page) - 1}"
            )
            cours = cursor.fetchone()[1:]

            await callback.message.edit_text(
                f"{cours[1]}\n\nНомер данного курса: {current_page}\n"
                f"Всего курсов: {PAGE_COUNT}\n\n{current_page}/{PAGE_COUNT}",
                reply_markup=url_cours
            )

    elif callback.data == 'Добавить':
        await callback.message.delete()
        await callback.message.answer(
            'Введите новый курс:',
            reply_markup=kb_adminback
        )
        await Form.add.set()

    elif callback.data.startswith('Редактировать'):
        course_id = int(callback.message.text.split('\n')[-1].split('/')[0])
        await callback.message.answer(
            'Введите отредактированный курс:',
            reply_markup=kb_adminback
        )
        await state.update_data(course_id=course_id)
        await Form.edit.set()

    elif callback.data.startswith('Удалить'):
        course_id = int(callback.message.text.split('\n')[-1].split('/')[0])
        cursor.execute(f"DELETE FROM courses WHERE id={course_id}")
        cursor.execute(
            f"UPDATE courses SET id = id - 1 WHERE id > {course_id}"
        )
        conn.commit()

        await callback.message.answer('Курс успешно удален!')
        await callback.message.answer(
            'Выберите пункт меню:',
            reply_markup=kb_admin
        )


async def cancel_handleradd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()

    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def finaledit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit'] = str(message.text)
    course_id = data['course_id']

    cursor = conn.cursor()
    cursor.execute(
        'UPDATE courses SET courses = ? WHERE id = ?',
        (data['edit'], int(course_id),)
    )
    conn.commit()

    await bot.send_message(
        message.from_user.id,
        'Курс изменен. База данных обновлена',
        reply_markup=kb_admin
    )
    await state.finish()

    await asyncio.sleep(1)
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )


async def finaladd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['add'] = str(message.text)

    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM courses')
    result = cursor.fetchone()

    new_id = 1 if result[0] is None else result[0] + 1
    cursor.execute(
        'INSERT INTO courses (id, courses) VALUES (?, ?)',
        (new_id, data['add'])
    )
    conn.commit()

    await bot.send_message(
        message.from_user.id,
        'Курс добавлен. База данных обновлена',
        reply_markup=kb_admin
    )
    await state.finish()

    await asyncio.sleep(1)
    await bot.send_message(
        message.from_user.id,
        'Выберите пункт меню:',
        reply_markup=kb_admin
    )
