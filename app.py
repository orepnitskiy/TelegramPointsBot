from aiogram import executor

from config.loader import bot, storage
from commands import dp
from middlewares import PointsMiddleware, RegistrationMiddleware
from database import setup_db



async def on_shutdown(dp):
    await bot.close()
    await storage.close()


async def on_startup(dp):
    await setup_db()

    dp.middleware.setup(RegistrationMiddleware())
    # dp.middleware.setup(PointsMiddleware())


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
