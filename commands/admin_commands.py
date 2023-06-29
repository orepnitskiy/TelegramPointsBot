from config import dp
from states import Setup, CallbackWait, UserStates, PointsSetup
from database import AdminPreferences, Contest, User
from filters import IsAdmin
from database import Admins
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


@dp.message_handler(IsAdmin(), commands='give_points')
async def give_points(message: types.Message):
    contest = await Contest.get(id=1)
    point_name = contest.point_name
    await message.answer(f'Tip protocol initialized. Who would you like to tip with {point_name}?')
    await UserStates.give_points_username.set()

# @dp.message_handler(Command('abort_command'), state="*")
# async def cmd_finish(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer('Command has been aborted')
#
#


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
    await message.answer('Instagram setup protocol initialized: In order to connect to your Instagram account '
                        'well need the API Key. Please input your Instagram API Key for now')

    await Setup.setup_instagram.set()


@dp.message_handler(IsAdmin(), commands='setup_instagram_hashtag')
async def setup_instagram_hashtag(message: types.Message):
    await message.answer("Hashtag protocol initialized. Please input the hashtag(s) "
                              "that you would like to monitor. If inputting multiple hashtags (up to 3) "
                              "please separate them by a ,")

    await Setup.setup_instagram_hashtag.set()


@dp.message_handler(IsAdmin(), commands='contest_name', state=None)
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


@dp.message_handler(IsAdmin(), commands='registration_active', state=None)
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


@dp.message_handler(IsAdmin(), commands='make_admin')
async def add_admin(message: types.Message):
    await message.answer('Initializing admin protocol. Please enter the username of the new Admin:')
    await UserStates.make_admin.set()


@dp.message_handler(IsAdmin(), commands='remove_admin')
async def remove_admin(message: types.Message):
    await message.answer('Initializing admin protocol. Please enter the username of the new Admin you would like to remove:')
    await UserStates.remove_admin.set()

@dp.message_handler(IsAdmin(), commands=['admin_list'])
async def admin_list_command(message: types.Message):
    # Fetch all admins from the database
    admins = await Admins.all()

    if admins:
        admin_list = "\n".join([f"ID: {admin.id}, Username: {admin.username}" for admin in admins])
        reply_message = f"Current admins:\n{admin_list}"
    else:
        reply_message = "There are no admins available."

    # Send the admin list as a reply
    await message.reply(reply_message)




b'{"carrier":"","city":"","country":"us","port":24000,"state":"","proxy_type":"persist","gb_cost":0.6,"mobile":false,' \
b'"unblock":false,"whitelist_ips":[],"account_id":"hl_a417b9ef","customer":"hl_a417b9ef","customer_id":"hl_a417b9ef",' \
b'"zone":"data_center","' \
b'password":"rmoosphkzb0x"}'


# data = {'proxy':{'port':24000,'zone': 'data_center','proxy_type':'persist','customer':'hl_a417b9ef','password':'rmoosphkzb0x','whitelist_ips':[]}}
# r = requests.put('http://127.0.0.1:22999/api/proxies/24000', data=json.dumps(data))
# print(r.content)
