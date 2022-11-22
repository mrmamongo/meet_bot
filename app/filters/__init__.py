from aiogram import Dispatcher

from app.filters.admin import AdminFilter
from app.filters.role import RoleFilter


def register_filters(dp: Dispatcher) -> None:
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
