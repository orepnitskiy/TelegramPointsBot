
from config import dp
from states import Setup, CallbackWait, UserStates, PointsSetup
from database import AdminPreferences, Contest, User
from filters import IsAdmin
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


# @dp.message_handler(commands=['user_setup'])
# async def user_setup_command(message: types.Message):
#     await message.reply(f"Welcome to asdasd- In order to get started with all of the amazing features you’ll "
#                         "need to run through the user setup menu! Would you like to proceed (Y/N)?")
#
#     # Set the user setup state
#     # await UserStates.user_setup.set()