import asyncio
import logging
from argparse import ArgumentParser
from typing import NoReturn

from app.config import settings
from app.main import main


def cli():
    try:
        logging.basicConfig(
            level=settings.get("LOG_LEVEL", "INFO"),
            format=settings.get("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
        )
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Exit")
