from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.orm import sessionmaker, Session

from app.services.poller import PollerService


class PollingMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["update"]

    def __init__(self, poller: PollerService):
        super().__init__()
        self.poller: PollerService = poller

    async def pre_process(self, obj, data, *args):
        data['poller']: PollerService = self.poller

    async def post_process(self, obj, data, *args):
        pass
