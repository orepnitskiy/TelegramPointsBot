from config import dp
from states import Setup, CallbackWait, UserStates
from database import AdminPreferences, Contest, User, Admins
from filters import IsAdmin

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from random import randint


@dp.message_handler(lambda message: message.text in ['Y', 'N'], state=CallbackWait.all_scores)
async def answer_all_scores(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        users = await User.all().distinct()
        d = []
        for user in users:
            d.append((user.name, round(user.points, 2)))

        stats = list(map(lambda x: f"username: {x[0]}, points: {x[1]}", d))
        data = ["User's scores:\n"]
        j = 0
        for i in stats:
            if len(data[j] + i + "\n") > 2000:
                data.append('')
                j += 1
            data[j] += i + "\n"
        for d in data:
            await message.answer(d)
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(lambda message: message.text in ['Y', 'N'], state=CallbackWait.top_ten)
async def answer_top_ten(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        users = await User.all().order_by('-points').limit(10).distinct()
        d = []
        for user in users:
            d.append((user.name, round(user.points, 2)))

        stats = list(map(lambda x: f"username: {x[0]}, points: {x[1]}", d))
        data = ["User's scores:\n"]
        j = 0
        for i in stats:
            if len(data[j] + i + "\n") > 2000:
                data.append('')
                j += 1
            data[j] += i + "\n"
        for d in data:
            await message.answer(d)
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(lambda message: message.text in ['Y', 'N'], state=CallbackWait.top_hundred)
async def answer_top_hundred(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        users = await User.all().order_by('-points').limit(100).distinct()
        d = []
        for user in users:
            d.append((user.name, round(user.points, 2)))

        stats = list(map(lambda x: f"username: {x[0]}, points: {x[1]}", d))
        data = ["Top 100 Leaderboard:\n"]
        j = 0
        for i in stats:
            if len(data[j] + i + "\n") > 2000:
                data.append('')
                j += 1
            data[j] += i + "\n"
        for d in data:
            await message.answer(d)
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(IsAdmin(), state=UserStates.give_points_username)
async def answer_give_points_username(message: types.Message, state: FSMContext):
    answer = message.text
    user = await User.get_or_none(name=answer)
    if user:
        await message.answer(f'Okay how many points would you like to tip {answer}')
        async with state.proxy() as data:
            data['username'] = answer
        await UserStates.give_points_count.set()
    else:
        await message.answer('User was not found')
        await state.finish()


@dp.message_handler(IsAdmin(), state=UserStates.give_points_count)
async def answer_give_points_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        username = data['username']
    try:
        count = float(message.text)
        user = await User.get(name=username)
        user.points += count
        await user.save()
        await message.answer(f'{user.name} has been issued {count} points')
    except:
        await message.answer(f'{message.text} is not a number')
    await state.finish()


@dp.message_handler(state=UserStates.reset_scores)
async def answer_reset_scores(message: types.Message, state:FSMContext):
    answer = message.text
    if answer == 'Y':
        await User.all().update(points=0)
        await message.answer('Scores have been zeroed!')
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(state=UserStates.reset_statistics)
async def answer_reset_statistics(message: types.Message, state:FSMContext):
    answer = message.text
    if answer == 'Y':
        await User.all().update(points=0, registration=False)
        await message.answer('Scores and registration status have been zeroed!')
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(state=UserStates.select_winner)
async def answer_select_winner(message: types.Message, state:FSMContext):
    answer = message.text
    if answer == 'Y':
        users = await User.all().distinct()
        await message.answer(f'Complete: The winner username is: {users[randint(0, len(users) - 1)].name}! '
                                  f'Would you like to roll again? [Y/N]?')

    else:
        await message.answer('Preparation stopped')
        await state.finish()


@dp.message_handler(state=CallbackWait.add_admin)
async def answer_add_admin(message: types.Message, state: FSMContext):
    await Admins.create(username=message.text)
    await message.answer(f'{message.text} was added to the admin list')
    await state.finish()