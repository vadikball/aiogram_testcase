from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from data_base import sqlite_db
from keyboards import admin_kb

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id, 'Что хозяин надо?',
        reply_markup=admin_kb.button_case_admin
    )
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await message.reply('Ok')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену')


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()


async def del_callback_run(callback: types.CallbackQuery):
    pizza_name = callback.data.replace('del ', '')
    await sqlite_db.sql_delete_command(pizza_name)
    await callback.answer(
        text='{0} удалена.'.format(pizza_name),
        show_alert=True
    )


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        menu = await sqlite_db.sql_read()
        for row in menu:
            await bot.send_photo(
                message.from_user.id,
                row[0],
                '{0}\nОписание: {1}, Цена: {2}'.format(row[1], row[2], row[-1])
            )
            await bot.send_message(
                message.from_user.id,
                '^^^',
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        'Удалить {0}'.format(row[1]),
                        callback_data='del {0}'.format(row[1])
                    )
                )
            )


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='загрузить', state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands='удалить')
