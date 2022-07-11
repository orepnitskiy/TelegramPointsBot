from config import dp
from states import Setup, CallbackWait, UserStates, PointsSetup
from database import AdminPreferences, Contest, User
from filters import IsAdmin

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('abort_command'), state="*")
async def cmd_finish(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Command has been aborted')


@dp.message_handler(IsAdmin(), commands='start_setup', state=None)
async def start_setup(message: types.Message):
    await message.answer(f'Welcome to {message.from_user.username} - In order to get started with all of the'
                              f' amazing features well need to run through setup menu! '
                              f'Would you like to proceed (Y/N)?')

    await Setup.start_setup.set()


@dp.message_handler(IsAdmin(), commands='server_name')
async def server_name(message: types.Message):
    await message.answer("Server naming initialized. What is the name of your server?")

    await Setup.server_name.set()



@dp.message_handler(IsAdmin(), commands='setup_twitter')
async def setup_twitter(message: types.Message):
    await message.answer('Twitter setup protocol initialized: In order to connect to your Twitter account '
                        'well need the API Key. Please input your Twitter API Key for now')

    await Setup.setup_twitter.set()


@dp.message_handler(IsAdmin(), commands='setup_twitter_hashtag')
async def setup_twitter_hashtag(message: types.Message):
    await message.answer("Hashtag protocol initialized. Please input the hashtag(s) "
                              "that you would like to monitor. If inputting multiple hashtags (up to 3) "
                              "please separate them by a ,")

    await Setup.setup_twitter_hashtag.set()


@dp.message_handler(IsAdmin(), commands='setup_instagram')
async def setup_instagram(message: types.Message):
    await message.answer('Twitter setup protocol initialized: In order to connect to your Instagram account '
                        'well need the API Key. Please input your Instagram API Key for now')

    await Setup.setup_instagram.set()


@dp.message_handler(IsAdmin(), commands='setup_instagram_hashtag')
async def setup_instagram_hashtag(message: types.Message):
    await message.answer("Hashtag protocol initialized. Please input the hashtag(s) "
                              "that you would like to monitor. If inputting multiple hashtags (up to 3) "
                              "please separate them by a ,")

    await Setup.setup_instagram_hashtag.set()


@dp.message_handler(IsAdmin(), commands='setup_contest_name', state=None)
async def setup_contest_name(message: types.Message):
    await message.answer('What is the name of your upcoming contest?')

    await Setup.contest_name.set()


@dp.message_handler(IsAdmin(), commands='setup_point_name', state=None)
async def setup_point_name(message: types.Message):
    await message.answer('What name do you want to give your point system?')

    await Setup.point_name.set()


@dp.message_handler(IsAdmin(), commands='setup_contest_start_date', state=None)
async def setup_contest_start_date(message: types.Message):
    await message.answer('What day would you like the contest to start? Please be sure to input the'
                                  'date in the following format: mm/dd/yyyy - '
                                  'If contest is to start manual simply input “none"')

    await Setup.contest_start_date.set()


@dp.message_handler(IsAdmin(), commands='setup_contest_end_date', state=None)
async def setup_contest_end_date(message: types.Message):
    await message.answer('What day would you like the contest to end? Please be sure to input the'
                                  'date in the following format: mm/dd/yyyy - '
                                  'If contest is to end manual simply input “none"')

    await Setup.contest_end_date.set()


@dp.message_handler(IsAdmin(), commands='start_contest', state=None)
async def start_contest(message: types.Message):
    await message.answer('Preparing for ignition. Are you sure you want to start the contest? (Y/N)')
    await CallbackWait.start_contest.set()


@dp.message_handler(IsAdmin(), commands='end_contest', state=None)
async def end_contest(message: types.Message):
    await message.answer('Preparing for ignition. Are you sure you want to end the contest? (Y/N)')
    await CallbackWait.end_contest.set()


@dp.message_handler(IsAdmin(), commands='pause_contest', state=None)
async def pause_contest(message: types.Message):
    await message.answer('Preparing for ignition. Are you sure you want to pause the contest? (Y/N)')
    await CallbackWait.pause_contest.set()


@dp.message_handler(IsAdmin(), commands='registration_open', state=None)
async def open_registration(message: types.Message):
    await message.answer('Are you sure you would like to open user registration? (Y/N)')
    await CallbackWait.open_registration.set()


@dp.message_handler(IsAdmin(), commands='registration_ended', state=None)
async def close_registration(message: types.Message):
    await message.answer('Are you sure you would like to close user registration? (Y/N)')
    await CallbackWait.close_registration.set()


@dp.message_handler(IsAdmin(), commands='tg_score_sent_message')
async def tg_score_sent_message(message: types.Message):
    await message.answer('What is the value of 1 sent message on Telegram?')
    await PointsSetup.tg_score_sent_message.set()


@dp.message_handler(IsAdmin(), commands='add_admin')
async def add_admin(message: types.Message):
    await message.answer('What is the username of the new admin without a "@"')
    await CallbackWait.add_admin.set()
