import logging

import nats
from aiogram import types, Bot, Dispatcher
from nats.aio.client import Client
from nats.js.kv import KeyValue

from app.FSMStorage import NATSFSMStorage
from app.filters import register_filters
from app.handlers import register_handlers
from app.middlewares import register_middlewares
from config import settings

logger = logging.getLogger(__name__)


async def init_nats_kv() -> tuple[Client, KeyValue, KeyValue]:
    nc = await nats.connect(settings.get("NATS_URL", "nats://localhost:4222"))
    js = nc.jetstream()
    kv_states = await js.key_value("aiogram_states")
    kv_data = await js.key_value("aiogram_data")
    return nc, kv_states, kv_data


async def on_startup(dp: Dispatcher) -> None:
    logger.info("Starting...")
    logger.info("NATS connected")
    register_middlewares(dp)
    register_filters(dp)
    register_handlers(dp)


async def on_shutdown(dp: Dispatcher) -> None:
    logger.warning("Shutting down...")
    await dp.storage.close()
    logger.warning("Exit")


async def main() -> None:
    try:
        nc, kv_states, kv_data = await init_nats_kv()
        bot = Bot(token=settings.telegram.TOKEN, parse_mode=types.ParseMode.HTML)
        dp = Dispatcher(storage=NATSFSMStorage(nc, kv_states, kv_data))

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)
        raise e
