import logging
import sqlite3

from aiogram.utils import executor

from create_bot import dp
from handlers import client, admin, other


logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('db.db')
cursor = conn.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS users '
    '(INTEGER PRIMARY KEY, userid TEXT, blacklist INTEGER DEFAULT 0)'
)

cursor.execute(
    'CREATE TABLE IF NOT EXISTS courses '
    '(INTEGER PRIMARY KEY, id INTEGER, courses TEXT)'
)
cursor.execute('SELECT id FROM courses WHERE id = 1')
checkc = cursor.fetchone()
if checkc is None:
    cursor.execute(
        'INSERT INTO courses (id, courses) VALUES (?, ?)',
        (1, 'NO_DATA',)
    )
    conn.commit()

cursor.execute(
    'CREATE TABLE IF NOT EXISTS discounts '
    '(id INTEGER PRIMARY KEY, discounts TEXT)'
)
cursor.execute('SELECT id FROM discounts WHERE id = 1')
checkd = cursor.fetchone()
if checkd is None:
    cursor.execute(
        'INSERT INTO discounts (discounts) VALUES (?)',
        ('NO_DATA',)
    )
    conn.commit()
conn.commit()


client.registere_handlers_client(dp)
admin.registere_handlers_admin(dp)
other.registere_handlers_other(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
