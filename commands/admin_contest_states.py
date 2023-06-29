from commands.admin_commands import add_admin, remove_admin
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
    mes = message.text
    answer = mes.split('@')[1]
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


@dp.message_handler(state=UserStates.make_admin)
async def answer_add_admin(message: types.Message, state: FSMContext):
    if '@' in message.text:
        account = message.text.split('@')[1]
    else:
        account = message.text
    await message.reply(f'{account} will be promoted to Admin. Is this correct? [Y/N]')
    await state.update_data(account=account)
    await UserStates.add_admin_yes_no.set()

@dp.message_handler(state=UserStates.remove_admin)
async def answer_remove_admin(message: types.Message, state: FSMContext):
    if '@' in message.text:
        account = message.text.split('@')[1]
    else:
        account = message.text
    await message.reply(f'{account} will be removed from Admins. Is this correct? [Y/N]')
    await state.update_data(account=account)
    await UserStates.remove_admin_yes_no.set()



@dp.message_handler(state=UserStates.add_admin_yes_no)
async def add_admin_yes_no(message: types.Message, state: FSMContext):
    data = await state.get_data()
    account = data.get('account')
    if message.text.lower() == 'y':
        await message.reply(f'Confirmed. {account} has been promoted to Admin.')
        await Admins.create(username=account)
        await state.finish()
    elif message.text.lower() == 'n':
        await message.reply('Sorry about that ')
        await add_admin(message)

    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")


@dp.message_handler(state=UserStates.remove_admin_yes_no)
async def remove_admin_yes_no(message: types.Message, state: FSMContext):
    data = await state.get_data()
    account = data.get('account')
    if message.text.lower() == 'y':
        await message.reply(f'Confirmed. {account} has been removed from Admin.')
        await Admins.delete(username=account)
        await state.finish()
    elif message.text.lower() == 'n':
        await message.reply('Sorry about that ')
        await remove_admin(message)
    else:
        await message.reply("Invalid response. Please select either 'Y' or 'N'.")





