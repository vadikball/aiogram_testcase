
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import Settings

settings = Settings()

storage = MemoryStorage()


bot = Bot(settings.token)
dp = Dispatcher(bot, storage=storage)
