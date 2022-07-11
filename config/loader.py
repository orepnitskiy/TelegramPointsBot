from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .const import TG_BOT_TOKEN


bot = Bot(token=TG_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


