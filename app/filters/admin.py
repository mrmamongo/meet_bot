from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject

from app.models.user import UserRole


class AdminFilter(BoundFilter):
    key = "admin"

    def __init__(self, admin: None | bool = True):
        self.admin = admin

    async def check(self, obj: TelegramObject) -> bool:
        if self.admin is None:
            return True
        data = ctx_data.get()
        return (data.get("role") is UserRole.ADMIN) == self.admin
