from config import dp
from states import Setup, CallbackWait, UserStates
from database import AdminPreferences, Contest, User
from filters import IsAdmin

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('abort_command'), state="*")
async def cmd_finish(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Command has been aborted')


@dp.message_handler(IsAdmin(), commands='all_scores')
async def all_scores(message: types.Message):
    await message.answer('Initializing score card protocol.')
    await message.answer('Protocol run complete - would you like to view? (Y/N)')
    await CallbackWait.all_scores.set()


@dp.message_handler(IsAdmin(), commands='top_ten')
async def top_ten(message: types.Message):
    await message.answer('Initializing score card protocol.')
    await message.answer('Protocol run complete - would you like to view? (Y/N)')
    await CallbackWait.top_ten.set()


@dp.message_handler(IsAdmin(), commands='leaderboard')
async def top_hundred(message: types.Message):
    await message.answer('Initializing score card protocol.')
    await message.answer('Protocol run complete - would you like to view? (Y/N)')
    await CallbackWait.top_hundred.set()


# @dp.message_handler(IsAdmin(), commands='give_points')
# async def give_points(message: types.Message):
#     contest = await Contest.get(id=1)
#     point_name = contest.point_name
#     await message.answer(f'Tip protocol initialized. Who would you like to tip with {point_name}? Input username without a "@"')
#     await UserStates.give_points_username.set()


@dp.message_handler(IsAdmin(), commands=['reset_scores'])
async def reset_scores(message: types.Message):
    print('asdasdasd')
    await message.answer('Score reset protocol has been initialized. All user scores will be reset to 0. '
                         'Are you sure you would like to proceed? (Y/N)')
    await UserStates.reset_scores.set()


@dp.message_handler(IsAdmin(), commands=['reset_statistics'])
async def reset_scores(message: types.Message):
    await message.answer('Score reset protocol has been initialized. All user scores will be reset to 0.'
                         'Registration status will be reset. '
                         'Are you sure you would like to proceed? (Y/N)')
    await UserStates.reset_statistics.set()


@dp.message_handler(IsAdmin(), commands=['select_winner'])
async def random_winner(message: types.Message):
    await message.answer('Initialization randomization protocol. Are you sure you want to roll the dice? (Y/N)')
    await UserStates.select_winner.set()

