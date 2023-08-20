from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data_base.sql_db import Database
import os


storage = MemoryStorage()

TOKEN = os.getenv('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
db = Database('database.db')

