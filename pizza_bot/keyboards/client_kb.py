from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton)

b1 = KeyboardButton('/режим_работы')
b2 = KeyboardButton('/расположение')
b3 = KeyboardButton('/меню')
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Где я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).insert(b3).row(b4, b5)

