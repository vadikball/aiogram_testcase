import hashlib

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import Settings

settings = Settings()

storage = MemoryStorage()


async def on_startup(_):
    print('Online...')


bot = Bot(settings.token)
dp = Dispatcher(bot, storage=storage)


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    link = 'https://ru.wikipedia.org/wiki/'+text
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [
        InlineQueryResultArticle(
            id=result_id,
            title='Статья Wiki:',
            url=link,
            input_message_content=InputTextMessageContent(
                message_text=link
            )
        )
    ]

    await query.answer(articles, cache_time=1, is_personal=True)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
