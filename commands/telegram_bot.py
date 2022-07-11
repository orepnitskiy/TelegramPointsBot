# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher import filters
#
# import config
# from config.loader import dp
# from states.setup import Setup
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['tg_score_invite'])
# async def tg_score_invite(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['tg_score_react'])
# async def tg_score_react(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['tg_score_sent_message'])
# async def tg_score_sent_message(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_score_hashtag'])
# async def instagram_score_hashtag(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_score_follow'])
# async def instagram_score_follow(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_score_comment'])
# async def instagram_score_comment(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_score_like'])
# async def instagram_score_like(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_score_hashtag'])
# async def twitter_score_hashtag(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_score_quote_tweet'])
# async def twitter_score_quote_tweet(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_score_retweet'])
# async def twitter_score_retweet(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_score_tweet_tagged'])
# async def twitter_score_tweet_tagged(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_score_tweet_like'])
# async def twitter_score_tweet_like(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_score_follow'])
# async def twitter_score_follow(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_retweet'])
# async def twitter_retweet(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_like'])
# async def twitter_like(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_follow'])
# async def twitter_follow(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['twitter_tag'])
# async def twitter_tag(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_comment'])
# async def instagram_comment(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_follow'])
# async def instagram_follow(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_hashtag'])
# async def instagram_hashtag(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['instagram_like'])
# async def instagram_like(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['reset_statistics'])
# async def reset_statistics(message: types.Message):
#     await message.answer('Hello')
#
#
# @dp.message_handler(filters.IDFilter(user_id=[config.TG_ADMIN_ID]), commands=['select_winner'])
# async def select_winner(message: types.Message):
#     await message.answer('Hello')
#