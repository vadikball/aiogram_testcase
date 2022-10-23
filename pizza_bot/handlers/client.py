import os
import traceback

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from create_bot import bot
from data_base import sqlite_db
from keyboards import client_kb
from settings import Settings

settings = Settings()


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id,
            'Приятного аппетита',
            reply_markup=client_kb.kb_client
        )
        await message.delete()
    except:
        print(traceback.format_exc())
        await message.reply(
            'Общение с ботом через лс,'
            'Напишите ему:\n{0}'.format(settings.bot_url)
        )


# @dp.message_handler(commands=['режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Вс-Чт с 9:00 до 20:00,'
        'Пт-Сб с 10:00 до 23:00'
    )


# @dp.message_handler(commands=['расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'ул. Колбасная 15',
        reply_markup=ReplyKeyboardRemove()
    )


# @dp.message_handler(commands=['меню'])
async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['меню'])
