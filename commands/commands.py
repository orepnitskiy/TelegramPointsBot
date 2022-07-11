from config import dp
from filters import IsContest, IsRegistration, IsNotRegistration, IsRegisteredToContest
from database import User, AdminPreferences
from states import UserStates

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('abort_command'), state="*")
async def cmd_finish(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Command has been aborted')


@dp.message_handler(IsRegistration(), commands='register')
async def register_on_contest(message: types.Message):
    user = await User.get(uid=message.from_user.id)
    if not user.registered:
        user.registered = True
        await user.save()
        await message.answer('You are now registered on the contest. \n'
                             'To earn more points add links write /register_twitter and /register_instagram')
    else:
        await message.answer('You are already registered on the contest')


@dp.message_handler(IsNotRegistration(), commands='register')
async def not_register_on_contest(message: types.Message):
    await message.answer('Sorry, the registration is ended.')


@dp.message_handler(IsRegisteredToContest(), commands='register_twitter')
async def register_twitter(message: types.Message):
    await message.answer('Write your twitter username (e.g. elonmusk)')
    await UserStates.twitter_answer.set()


@dp.message_handler(IsRegisteredToContest(), commands='register_instagram')
async def register_instagram(message: types.Message):
    await message.answer('Write your instagram username (e.g. elonmusk)')
    await UserStates.instagram_answer.set()


@dp.message_handler(commands='check_score')
async def check_score(message: types.Message):
    user = await User.get(uid=message.from_user.id)
    await message.answer(f'Your current score is: {round(user.points, 2)}')


@dp.message_handler(commands='transfer_points')
async def transfer_points(message: types.Message):
    await message.answer('Transfer protocol initialized, please input the name of the user you would '
                    'like to receive the transfer (without a "@")')
    await UserStates.transfer_points_username.set()


@dp.message_handler(IsContest(), IsRegisteredToContest(), content_types=['text', 'sticker'])
async def points(message: types.Message):
    user = await User.get(uid=message.from_user.id)

    admins_config = await AdminPreferences.get_or_none(id=1)
    if not admins_config:
        admins_config = await AdminPreferences.create(id=1)
    points = admins_config.sent_message
    user.points += points
    await user.save()


@dp.message_handler(IsContest(), IsRegisteredToContest(), content_types='voice')
async def points(message: types.Message):
    user = await User.get(uid=message.from_user.id)
    admins_config = await AdminPreferences.get_or_none(id=1)
    if not admins_config:
        admins_config = await AdminPreferences.create(id=1)
    points = admins_config.voice * message.voice.duration
    user.points += points
    await user.save()

