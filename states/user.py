from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    wait_for_answer = State()
    twitter_answer = State()
    instagram_answer = State()
    give_points_username = State()
    give_points_count = State()
    transfer_points_username = State()
    transfer_points_count = State()
    reset_scores = State()
    reset_statistics = State()
    select_winner = State()


class CallbackWait(StatesGroup):
    start_contest = State()
    end_contest = State()
    pause_contest = State()
    open_registration = State()
    close_registration = State()
    all_scores = State()
    top_ten = State()
    top_hundred = State()
    add_admin = State()
