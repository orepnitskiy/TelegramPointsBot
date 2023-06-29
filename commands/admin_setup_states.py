from commands.admin_commands import server_name, setup_twitter, setup_twitter_hashtag, setup_instagram, \
    setup_instagram_hashtag, setup_contest_name, setup_point_name, setup_contest_start_date, setup_contest_end_date
from config import dp
from states import Setup, CallbackWait, UserStates, PointsSetup
from database import AdminPreferences, Contest, User
from filters import IsAdmin

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from datetime import datetime


@dp.message_handler(Command('abort_command'), state="*")
async def cmd_finish(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Command has been aborted')


@dp.message_handler(IsAdmin(), state=Setup.start_setup)
async def answer_start_setup(message: types.Message, state: FSMContext):
    if message.text.lower() == 'y':
        await message.answer('Ok lets get started - well start with the server name '
                             '(Advances to server name and activates auto advance)')
        await state.finish()
        await server_name(message)
    if message.text.lower() == 'n':
        await message.reply('Configuration has been canceled!')
        await state.finish()



@dp.message_handler(IsAdmin(), state=Setup.server_name)
async def answer_server_name(message: types.Message, state: FSMContext):
    answer = message.text
    await message.answer(f'Ok, from now your server will be called {answer}')
    contest = await Contest.get_or_none(id=1)
    if not contest:
        contest = await Contest.create()
    contest.server_name = answer
    await contest.save()
    await state.finish()
    await setup_twitter(message)
    # else:
    #     await message.answer('Configuration is finished')
    #     await state.finish()


@dp.message_handler(IsAdmin(), state=Setup.setup_twitter)
async def answer_setup_twitter(message: types.Message, state: FSMContext):
    answer = message.text
    # Check api key
    is_key = True
    if is_key:
        await message.answer(f'Thanks! We have successfully connected to twitter account {answer}')
        prefs = await AdminPreferences.get_or_none(id=1)
        if not prefs:
            prefs = await AdminPreferences.create(id=1)
        prefs.twitter_api_key = answer
        await prefs.save()
        await state.finish()
        await setup_twitter_hashtag(message)

    else:
        await message.answer("Hmm, that doesn't seem quite right. Lets try that one more time...")
        await state.finish()
        await setup_twitter(message)

@dp.message_handler(IsAdmin(), state=Setup.setup_twitter_hashtag)
async def answer_setup_twitter_hashtag(message: types.Message, state: FSMContext):
    answer = message.text
    hashtags = answer.split(',')
    if len(hashtags) <= 3:
        valid_hashtags = [tag for tag in hashtags if tag.startswith('#')]
        if len(valid_hashtags) > 0:

            await message.answer('Thanks! Hashtags have been successfully entered')
            prefs = await AdminPreferences.get(id=1)
            prefs.twitter_hashtags = valid_hashtags
            await prefs.save()
            await state.finish()
            await setup_instagram(message)
        else:
            await message.answer("Invalid hashtags. Please make sure each hashtag starts with '#' "
                                 "and separate multiple hashtags with a comma (,).")
            await state.finish()
            await setup_twitter_hashtag(message)
    else:
        await message.answer("Please re-enter the hashtag(s) that you would like to monitor. If inputting "
                                    "multiple hashtags (up to 3) please separate them by a ','")
        await state.finish()
        await setup_twitter_hashtag(message)

    # return


@dp.message_handler(IsAdmin(), state=Setup.setup_instagram)
async def answer_setup_instagram(message: types.Message, state: FSMContext):
    answer = message.text
    # Check api key
    is_key = True
    if is_key:
        await message.answer(f'Thanks! We have successfully connected to Instagram account {answer}')
        prefs = await AdminPreferences.get(id=1)
        prefs.instagram_api_ley = answer
        await prefs.save()
        await state.finish()
        await setup_instagram_hashtag(message)
    else:
        await message.answer("Hmm, that doesn't seem quite right. Lets try that one more time...")
        await state.finish()
        await setup_instagram(message)



@dp.message_handler(IsAdmin(), state=Setup.setup_instagram_hashtag)
async def answer_setup_instagram_hashtag(message: types.Message, state: FSMContext):
    answer = message.text
    hashtags = answer.split(',')
    if len(hashtags) <= 3:
        valid_hashtags = [tag for tag in hashtags if tag.startswith('#')]
        if len(valid_hashtags) > 0:

            await message.answer('Thanks! Hashtags have been successfully entered')
            prefs = await AdminPreferences.get(id=1)
            prefs.instagram_hashtags = ', '.join(valid_hashtags)
            await prefs.save()
            await state.finish()
            await setup_contest_name(message)
        else:
            await message.answer("Invalid hashtags. Please make sure each hashtag starts with '#' "
                                 "and separate multiple hashtags with a comma (,).")
            await state.finish()
            await setup_instagram_hashtag(message)
    else:
        await message.answer("Please re-enter the hashtag(s) that you would like to monitor. If inputting "
                                    "multiple hashtags (up to 3) please separate them by a ','")
        await state.finish()
        await setup_instagram_hashtag(message)

@dp.message_handler(IsAdmin(), state=Setup.contest_name)
async def answer_contest_name(message: types.Message, state: FSMContext):
    answer = message.text
    await message.answer(f'Sounds great, your new contest is called {answer}')
    contest = await Contest.get(id=1)
    contest.contest_name = answer
    await contest.save()
    await state.finish()
    await setup_point_name(message)


@dp.message_handler(IsAdmin(), state=Setup.point_name)
async def answer_point_name(message: types.Message, state: FSMContext):
    answer = message.text
    await message.answer(f'Okay! From now on your points will be called {answer}')
    contest = await Contest.get(id=1)
    contest.point_name = answer
    await contest.save()
    await state.finish()
    await setup_contest_start_date(message)



@dp.message_handler(IsAdmin(), state=Setup.contest_start_date)
async def answer_contest_start_date(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        datetime.strptime(answer, '%m/%d/%Y')
        await message.answer(f'Alright! We have set your contest start date for {answer}')
        contest = await Contest.get(id=1)
        contest.contest_start_date = answer
        await contest.save()
        await state.finish()
        await setup_contest_end_date(message)
    except:
        if answer.lower() == 'none':
            contest = await Contest.get(id=1)
            contest.contest_start_date = answer
            await contest.save()
            await state.finish()
            # await setup_contest_end_date(message)
        else:
            await message.answer('Incorrect datetime format, try one more time...')
            await state.finish()
            await setup_contest_start_date(message)



@dp.message_handler(IsAdmin(), state=Setup.contest_end_date)
async def answer_contest_end_date(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        datetime.strptime(answer, '%m/%d/%Y')
        await message.answer(f'Alright! We have set your contest end date for {answer}')
        contest = await Contest.get(id=1)
        contest.contest_end_date = answer
        await contest.save()
        await state.finish()
    except:
        if answer.lower() == 'none':
            contest = await Contest.get(id=1)
            contest.contest_end_date = answer
            await contest.save()
            await state.finish()
        else:
            await message.answer('Incorrect datetime format, try one more time...')
            await setup_contest_end_date(message)
    # await state.finish()


@dp.message_handler(IsAdmin(), state=CallbackWait.start_contest)
async def answer_start_contest(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        contest = await Contest.get(id=1)
        contest.manual_contest_status = 'started'
        await contest.save()
        await message.answer('Contest started!')
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(IsAdmin(), state=CallbackWait.end_contest)
async def answer_ended_contest(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        contest = await Contest.get(id=1)
        contest.manual_contest_status = 'ended'
        await contest.save()
        await message.answer('Contest ended!')
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(IsAdmin(), state=CallbackWait.pause_contest)
async def answer_pause_contest(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        contest = await Contest.get(id=1)
        contest.manual_contest_status = 'paused'
        await contest.save()
        await message.answer('Contest paused!')
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(IsAdmin(), state=CallbackWait.open_registration)
async def answer_open_registration(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        contest = await Contest.get(id=1)
        contest.registration_status = True
        await contest.save()
        await message.answer('User registration is now open!')
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(IsAdmin(), state=CallbackWait.close_registration)
async def answer_close_registration(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Y':
        contest = await Contest.get(id=1)
        contest.registration_status = False
        await contest.save()
        await message.answer('User registration is now closed!')
    else:
        await message.answer('Preparation stopped')
    await state.finish()


@dp.message_handler(IsAdmin(), state=PointsSetup.tg_score_sent_message)
async def answer_score_sent_message(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        score = float(answer)
        contest = await AdminPreferences.get(id=1)
        contest.sent_message = score
        await contest.save()
        await message.answer(f'Thank you! The value of 1 message is set to {score}')
    except:
        await message.answer(f'{answer} is not a digit...')
    await state.finish()
