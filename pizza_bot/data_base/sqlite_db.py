import sqlite3 as sq
from sqlite3 import Connection, Cursor
from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram import types
from create_bot import bot

base: Optional[Connection] = None
cur: Optional[Cursor] = None


def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)"""
    )
    base.commit()


async def sql_add_command(state: FSMContext):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO menu VALUES (?, ?, ?, ?)',
            tuple(data.values())
        )
        base.commit()


async def sql_read(message: Optional[types.Message] = None):
    query = """ SELECT * FROM menu """
    if message is None:
        return cur.execute(query).fetchall()

    for row in cur.execute(query).fetchall():
        await bot.send_photo(
            message.from_user.id,
            row[0],
            '{0}\nОписание: {1}, Цена: {2}'.format(row[1], row[2], row[-1])
        )


async def sql_delete_command(pizza_name: str):
    cur.execute(
        'DELETE FROM menu WHERE name == ?',
        (pizza_name, )
    )
    base.commit()
