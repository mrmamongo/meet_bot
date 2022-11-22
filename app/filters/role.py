from typing import Any, Union, Dict

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message
from aiogram.types.base import TelegramObject
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import UserRole, User


class RoleFilter(BaseFilter):
    key = "role"

    def __init__(self,
                 session: Session,
                 role: list[UserRole] | UserRole | None = None,
                 **data: Any
                 ):
        super().__init__(**data)
        self.session: Session = session
        if isinstance(role, list):
            self.role: list[UserRole] = role
        elif isinstance(role, UserRole):
            self.role: list[UserRole] = [role]
        else:
            self.role: list[UserRole] = []

    async def __call__(self, message: Message) -> bool:
        user = self.session.execute(select(User).where(User.id == message.from_user.id)).one_or_none()
        return user.role in self.role
