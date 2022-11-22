from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

Base = declarative_base()


async def create_pool() -> sessionmaker:
    engine = create_async_engine(
        f"{settings.database.DRIVER}://{settings.database.USER}:{settings.database.PASSWORD}"
        f"@{settings.database.HOST}:{settings.database.PORT}/{settings.database.DATABASE}",
    )
    return sessionmaker(engine, expire_on_commit=False, autoflush=False, class_=AsyncSession)

session = create_pool()