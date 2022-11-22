from aiogram import Dispatcher

from app.middlewares.database import DatabaseMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    dp.middleware.setup(DatabaseMiddleware(pool=create_pool))

