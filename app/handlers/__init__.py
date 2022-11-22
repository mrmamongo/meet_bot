from aiogram import Dispatcher

from .admin import router as admin_router
from .vip import router as vip_router
from .user import router as user_router

def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(vip_router)
