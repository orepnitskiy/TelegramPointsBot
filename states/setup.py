from aiogram.dispatcher.filters.state import StatesGroup, State


class Setup(StatesGroup):
    start_setup = State()
    server_name = State()
    setup_twitter = State()
    setup_twitter_hashtag = State()
    setup_instagram = State()
    setup_instagram_hashtag = State()
    contest_name = State()
    point_name = State()
    contest_start_date = State()
    contest_end_date = State()


class PointsSetup(StatesGroup):
    tg_score_invite = State()
    tg_score_react = State()
    tg_score_sent_message = State()
    instagram_score_hashtag = State()
    instagram_score_follow = State()
    instagram_score_comment = State()
    instagram_score_like = State()
    twitter_score_hashtag = State()
    twitter_score_quote_tweet = State()
    twitter_score_retweet = State()
    twitter_score_tweet_tagged = State()
    twitter_score_tweet_like = State()
    twitter_score_follow = State()
    twitter_retweet = State()
    twitter_like = State()
    twitter_follow = State()
    twitter_tag = State()
    instagram_comment = State()
    instagram_follow = State()
    instagram_hashtag = State()
    instagram_like = State()

