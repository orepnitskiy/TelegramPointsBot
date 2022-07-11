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


@dp.message_handler(IsRegisteredToContest(), state=UserStates.twitter_answer)
async def answer_register_twitter(message: types.Message, state: FSMContext):
    username_check = True
    if username_check:
        user = await User.get(uid=message.from_user.id)
        user.twitter_username = message.text
        await user.save()
        await message.answer(f'Your twitter username is set to {message.text}')
        await state.finish()
    else:
        await message.answer(f'Sorry, we cannot validate your username, try one more time...')
        return


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