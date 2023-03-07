from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


b1 = KeyboardButton('Изменить информацию о курсах')
b2 = KeyboardButton('Изменить информацию о скидках')
b3 = KeyboardButton('Создать рассылку')
b4 = KeyboardButton('Вернуться в админ-меню')
b5 = KeyboardButton('Выйти из Админ-Панели')
b6 = KeyboardButton('Управление пользователями')
b7 = KeyboardButton('Заблокировать пользователя')
b8 = KeyboardButton('Разблокировать пользователя')
b9 = KeyboardButton('Статус пользователя')
b10 = KeyboardButton('Статистика')
b11 = KeyboardButton('Добавить новый курс')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_adminback = ReplyKeyboardMarkup(resize_keyboard=True)
kb_adminremove = ReplyKeyboardMarkup(resize_keyboard=True)
kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)


kb_admin.add(b1).add(b2).add(b3).add(b6).add(b5)
kb_adminback.add(b4)
kb_clients.add(b7).add(b8).add(b9).add(b10).add(b4)


urlb1 = InlineKeyboardButton('ᐅ', callback_data='Вперед')
urlb2 = InlineKeyboardButton('ᐊ', callback_data='Назад')
urlb3 = InlineKeyboardButton('Редактировать', callback_data='Редактировать')
urlb4 = InlineKeyboardButton('Удалить', callback_data='Удалить')
urlb5 = InlineKeyboardButton('Добавить', callback_data='Добавить')
url6 = InlineKeyboardButton('Добавить фотографию', callback_data='add_photo')
url7 = InlineKeyboardButton('Разослать', callback_data='next')
url8 = InlineKeyboardButton('Отменить', callback_data='otmena')


url_cours = InlineKeyboardMarkup(row_width=2)
url_spam = InlineKeyboardMarkup(row_width=2)
url_spamf = InlineKeyboardMarkup()


url = [
    InlineKeyboardButton('ᐊ', callback_data='Назад'),
    InlineKeyboardButton('ᐅ', callback_data='Вперед')
]

url_cours.row(*url).add(urlb3).add(urlb4).add(urlb5)
url_spam.add(url6).add(url7).add(url8)
url_spamf.add(url7).add(url8)
