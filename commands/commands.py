import time
import uuid
from aiogram.utils import markdown

from config import dp, bot
from filters import IsContest, IsRegistration, IsNotRegistration, IsRegisteredToContest
from database import User, AdminPreferences
from states import UserStates

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


# @dp.message_handler(Command('skip'), state="*")
# async def skip_command(message: types.Message, state: FSMContext):
#     await message.reply("Skip protocol initialized - are you sure you want to skip the current state? [Y/N]")
#     await UserStates.skip_confirmation.set()
#
# state_stack = []
# @dp.message_handler(state=UserStates.skip_confirmation)
# async def skip_confirmation(message: types.Message, state: FSMContext):
#     if message.text.lower() == 'y':
#         await message.reply("Command skipped.")
#         next_state = state_stack.pop()  # Retrieve the next state from the stack
#         await next_state.set()  # Set the next state
#         await next_state.handler(message)  # Execute the handler for the next state
#     elif message.text.lower() == 'n':
#         if state_stack:
#             previous_state = state_stack.pop()  # Retrieve the previous state from the stack
#             await message.reply("Skipping canceled. Returning to previous state.")
#             await previous_state.set()  # Set the state to the previous state
#         else:
#             await message.reply("Skipping canceled. No previous state found.")
#     else:
#         await message.reply("Invalid response. Please select either 'Y' or 'N'.")


@dp.message_handler(Command('abort_command'), state="*")
async def cmd_finish(message: types.Message, state: FSMContext):
    await state.finish()
    print(message.from_user.id)
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


# @dp.message_handler(IsRegisteredToContest(), commands='register_twitter')
# async def register_twitter(message: types.Message):
#     await message.answer('Write your twitter username (e.g. elonmusk)')
#     await UserStates.twitter_answer.set()


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


@dp.message_handler(commands=['user_setup'])
async def user_setup_command(message: types.Message):
    await message.reply(f"Welcome to 'asdsad' - In order to get started with all of the amazing features you’ll "
                        "need to run through the user setup menu! Would you like to proceed (Y/N)?")
    await UserStates.user_setup.set()


@dp.message_handler(commands=['username'])
async def username_command(message: types.Message):
    username = message.from_user.username
    await message.answer(f"Username confirmation protocol initialized. Your current user name is {username}, is this correct (Y/N)")
    await UserStates.username.set()


@dp.message_handler(commands=['register_wallet'])
async def register_wallet_command(message: types.Message):
    await message.answer(f"Wallet protocol initialized! Please enter your Bep-20 (Binanace Smart Chain) address here:")
    await UserStates.register_wallet.set()



@dp.message_handler(commands=['register_twitter'])
async def register_twitter_command(message: types.Message):
    await message.answer(f'Twitter registration protocol initialized! Please enter your Twitter username here:')
    await UserStates.register_twitter.set()


@dp.message_handler(commands=['register_instagram'])
async def register_instagram_command(message: types.Message):
    await message.answer(f'Instagram registration protocol initialized! Please enter your Instagram username here:')
    await UserStates.register_instagram.set()


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

@dp.message_handler(IsRegisteredToContest(), commands=['invite_link'])
async def invite_link(message: types.Message):
    chat_id = message.chat.id
    invite_link = await message.bot.create_chat_invite_link(chat_id)
    await message.reply(f"Here's the invite link for this chat:\n{invite_link.invite_link}")









