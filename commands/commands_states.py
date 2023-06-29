from commands.commands import username_command, register_wallet_command, register_twitter_command, \
    register_instagram_command
from config import dp
from states import UserStates
from database import AdminPreferences, Contest, User
from filters import IsRegisteredToContest

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('abort_command'), state="*")
async def cmd_finish(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Command has been aborted')


# @dp.message_handler(IsRegisteredToContest(), state=UserStates.twitter_answer)
# async def answer_register_twitter(message: types.Message, state: FSMContext):
#     username_check = True
#     if username_check:
#         user = await User.get(uid=message.from_user.id)
#         user.twitter_username = message.text
#         await user.save()
#         await state.finish()
#     else:
#         await message.answer(f'Sorry, we cannot validate your username, try one more time...')
#         return


@dp.message_handler(IsRegisteredToContest(), state=UserStates.instagram_answer)
async def answer_register_instagram(message: types.Message, state: FSMContext):
    username_check = True
    if username_check:
        user = await User.get(uid=message.from_user.id)
        user.instagram_username = message.text
        await user.save()
        await message.answer(f'Your instagram username is set to {message.text}')
        await state.finish()
    else:
        await message.answer(f'Sorry, we cannot validate your username, try one more time...')
        return


@dp.message_handler(state=UserStates.transfer_points_username)
async def answer_transfer_points_username(message: types.Message, state: FSMContext):
    answer = message.text
    user = await User.get_or_none(name=answer)
    if user:
        await message.answer(f'Perfect! Please input the amount of points '
                                      f'that you would like to transfer to {answer}')
        async with state.proxy() as data:
            data['username_transfer'] = answer
        await UserStates.transfer_points_count.set()
    else:
        await message.answer('User was not found')
        await state.finish()


@dp.message_handler(state=UserStates.transfer_points_count)
async def answer_transfer_points_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        username = data['username_transfer']
    try:
        count = float(message.text)
        sender = await User.get(uid=message.from_user.id)
        if sender.points <= count:
            sender.points -= count
            await sender.save()
            user = await User.get(name=username)
            user.points += count
            await user.save()
            await message.answer(f'You have transferred {count} point(s) to {user.name}')
        else:
            await message.answer("You don't have enought points")
    except:
        await message.answer(f'{message.text} is not a number')
    await state.finish()



@dp.message_handler(state=UserStates.user_setup)
async def answer_setup(message, state: FSMContext):
    print(message.text)
    if message.text.lower() == 'y':
        await message.reply(f"Ok lets get started - well start with your username and wallet")
        # await UserStates.username.set()
        await state.finish()
        await username_command(message)
    elif message.text.lower() == 'n':
        await message.reply("User configuration has been canceled!")
        await state.finish()
    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")



@dp.message_handler(state=UserStates.username)
async def username_setup(message, state: FSMContext):
    print(message.text)
    if message.text.lower() == 'y':
        username = message.from_user.username
        await message.reply(f"Thank you {username}, your Telegram username has been confirmed.")
        user, _ = await User.get_or_create(uid=message.from_user.id)
        user.registered = True
        user.confirmed = True
        user.confirmed_username = '@' + message.from_user.username
        await user.save()
        await state.finish()
        await register_wallet_command(message)
    elif message.text.lower() == 'n':
        await message.reply("Sorry about that, would you like to manually enter your username? [Y/N]")
        await state.finish()
        await UserStates.username_manually.set()

    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")


@dp.message_handler(state=UserStates.username_manually)
async def username_manually_setup(message, state: FSMContext):
    if message.text.lower() == 'y':
        await message.reply(f"Please manually enter your Telegram username(@)")
        await UserStates.USERNAME_CONFIRMED.set()
    elif message.text.lower() == 'n':
        await message.reply(f"Protocol aborted, please re-initialize if needed")
        await state.finish()
    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")


@dp.message_handler(state=UserStates.USERNAME_CONFIRMED)
async def username_confirmed(message, state: FSMContext):
    username = message.text

    await message.reply(f"Manual input confirmed, {username} has been confirmed as your username.")
    user, _ = await User.get_or_create(uid=message.from_user.id)
    user.registered = True
    user.confirmed = True
    user.confirmed_username = username
    await user.save()
    await state.finish()
    await register_wallet_command(message)


@dp.message_handler(state=UserStates.register_wallet)
async def register_wallet_setup(message, state: FSMContext):
    bsc = message.text
    if bsc.startswith('0x'):
        await message.reply(f"Thanks! Just to confirm, your wallet address is: {bsc} is this correct? (Y/N)")
        await UserStates.register_wallet_confirm.set()
        await state.update_data(bsc=bsc)


    elif not bsc.startswith('0x'):
        await message.reply("Hmm, that doesn't seem quite right. Lets try that one more time...Please enter a valid BSC address:")




@dp.message_handler(state=UserStates.register_wallet_confirm)
async def register_wallet_setup(message, state: FSMContext):
    if message.text.lower() == 'y':
        data = await state.get_data()
        bsc = data.get('bsc')
        await message.reply(f'Address confirmed! Thanks! We have successfully registered the following address: {bsc}')
        user, _ = await User.get_or_create(uid=message.from_user.id)
        user.bsc = bsc
        await user.save()
        await state.finish()
        await register_twitter_command(message)
    elif message.text.lower() == 'n':
        await message.reply(f"Sorry about that, let's try that again! Please re-enter your Binnance Smart Chain address:")
        await state.reset_state()
        await UserStates.register_wallet.set()
    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")


@dp.message_handler(state=UserStates.register_twitter)
async def register_twitter(message, state:FSMContext):
    twitter_account = message.text
    await message.reply(f'Perfect! Your Twitter name has been listed as {twitter_account},is this correct? [Y/N]')
    await state.update_data(twitter_account=twitter_account)
    await UserStates.register_twitter_setup.set()

@dp.message_handler(state=UserStates.register_twitter_setup)
async def register_twitter_setup(message, state:FSMContext):
    if message.text.lower() == 'y':
        data = await state.get_data()
        twitter_account = data.get('twitter_account')
        await message.reply(f'Perfect, we have confirmed your Twitter username as, {twitter_account}.')
        user, _ = await User.get_or_create(uid=message.from_user.id)
        user.twitter_username = twitter_account
        await user.save()
        await state.finish()
        await register_instagram_command(message)
    elif message.text.lower() == 'n':
        await message.reply(f'Sorry about that - lets try again! Please re-enter your Twitter username:')
        await UserStates.register_twitter.set()
    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")



@dp.message_handler(state=UserStates.register_instagram)
async def register_instagram(message, state:FSMContext):
    instagram_account = message.text
    await message.reply(f'Perfect! Your Instagram name has been listed as {instagram_account},is this correct? [Y/N]')
    await state.update_data(instagram_account=instagram_account)
    await UserStates.register_instagram_setup.set()


@dp.message_handler(state=UserStates.register_instagram_setup)
async def register_instagram_setup(message, state:FSMContext):
    if message.text.lower() == 'y':
        data = await state.get_data()
        instagram_account = data.get('instagram_account')
        await message.reply(f'Perfect, we have confirmed your Instagram username as, {instagram_account}.')
        user, _ = await User.get_or_create(uid=message.from_user.id)
        user.instagram_username = instagram_account
        await user.save()
        await state.finish()
    elif message.text.lower() == 'n':
        await message.reply(f'Sorry about that - lets try again! Please re-enter your Instagram username:')
        await UserStates.register_instagram.set()
    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")

