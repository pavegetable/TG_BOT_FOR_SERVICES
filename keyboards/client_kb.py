from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


b1 = KeyboardButton('Подать заявку')
b2 = KeyboardButton('Консультация')
b3 = KeyboardButton('Контакты')
b4 = KeyboardButton('Вернуться в меню')
b5 = KeyboardButton('Узнать о курсах в студии')
b6 = KeyboardButton('Узнать о скидках')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)


kb_client.add(b1).add(b5).add(b6).add(b3)
kb_menu.add(b4)


urlb1 = InlineKeyboardButton('Сайт', 'http://www.example.ru')
urlb2 = InlineKeyboardButton('ВКонтакте', 'https://vk.com/example')
urlb3 = InlineKeyboardButton('Телеграмм', 'https://t.me/example')
urlb4 = InlineKeyboardButton('ᐅ', callback_data='Впередк')
urlb5 = InlineKeyboardButton('ᐊ', callback_data='Назадк')
url6 = InlineKeyboardButton('Подать заявку', callback_data='Подать заявку')


url_coursс = InlineKeyboardMarkup(row_width=2)


url = [
    InlineKeyboardButton('ᐊ', callback_data='Назадк'),
    InlineKeyboardButton('ᐅ', callback_data='Впередк')
]


url_coursс.row(*url).add(url6)


url_con = InlineKeyboardMarkup(row_width=1)


url_con.add(urlb1).add(urlb2).add(urlb3)
