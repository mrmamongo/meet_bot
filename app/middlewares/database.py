from typing import Callable, Dict, Any, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.orm import sessionmaker, Session


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        pass

    skip_patterns = ["update"]

    def __init__(self, pool: sessionmaker):
        super().__init__()
        self.pool: sessionmaker = pool

    async def pre_process(self, obj, data, *args):
        session = self.pool()
        data["session"]: Session = session

    async def post_process(self, obj, data, *args):
        if session := data.get("session", None):
            await session.close()
