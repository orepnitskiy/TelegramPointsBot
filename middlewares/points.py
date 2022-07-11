from config import dp
from database import User, AdminPreferences
from filters import IsContest

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class PointsMiddleware(BaseMiddleware):

    @staticmethod
    async def on_process_message(message: types.Message, data: dict):

        user = await User.get(uid=message.from_user.id)

        admins_config = await AdminPreferences.get_or_none(id=1)
        if not admins_config:
            admins_config = await AdminPreferences.create(id=1)
        points = admins_config.sent_message
        user.points += points
        await user.save()
