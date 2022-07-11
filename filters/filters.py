from aiogram import types
from aiogram.dispatcher.filters import Filter

from database import Contest, User, Admins
from config.const import TG_ADMIN_ID

from datetime import datetime


class IsAdmin(Filter):
    async def check(self, message: types.Message) -> bool:
        user = await Admins.get_or_none(uid=message.from_user.id)
        if not user:
            user = await Admins.get_or_none(username=message.from_user.username)
        if not user and not TG_ADMIN_ID == message.from_user.id:
            return False
        else:
            return True


class IsRegistration(Filter):
    async def check(self, message: types.Message) -> bool:
        contest = await Contest.get(id=1)
        registration = contest.registration_status
        return registration


class IsNotRegistration(Filter):
    async def check(self, message: types.Message) -> bool:
        contest = await Contest.get(id=1)
        registration = contest.registration_status
        return not registration


class IsContest(Filter):
    async def check(self, message: types.Message) -> bool:
        contest = await Contest.get_or_none(id=1)
        if not contest:
            contest = await Contest.create(id=1)
            await contest.save()
        manual_control_status = contest.manual_contest_status
        start_date = contest.contest_start_date
        end_date = contest.contest_end_date
        try:
            start_date = datetime.strptime(start_date, '%m/%d/%Y')
            end_date = datetime.strptime(end_date, '%m/%d/%Y')
        except:
            start_date = None
            end_date = None

        date_now = datetime.now()

        if manual_control_status == "ended" or manual_control_status == "paused":
            return False
        elif manual_control_status == 'started':
            return True
        elif start_date == None or end_date == None:
            return False
        elif start_date <= date_now <= end_date or manual_control_status == 'started':
            return True


class IsRegisteredToContest(Filter):
    async def check(self, message: types.Message) -> bool:
        user = await User.get_or_none(uid=message.from_user.id)
        registered = user.registered
        return registered
