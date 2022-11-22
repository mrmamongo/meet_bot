from typing import List

from aiogram import Dispatcher
from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from app.models.user import User


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class PollerService(metaclass=SingletonMeta):
    def __init__(self, dp: Dispatcher, session: Session):
        self._dp = dp
        self._session = session

    def poll_location(self, location: dict[str, float]) -> list[Row | Row]:
        nearest_users = self._session.execute(
            select(User).where(User.location == location)
        ).all()
        return nearest_users

