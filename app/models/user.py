from enum import StrEnum

from sqlalchemy import Column, Integer, Enum, JSON, String, DateTime

from app.models.base import Base


class UserRole(StrEnum):
    """ Represents user roles """

    ADMIN = "admin"
    VIP = "vip"
    USER = "user"
    # BANNED = "banned" ??


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    location = Column(JSON, nullable=True)
    last_poll = Column(DateTime, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, role={self.role})"
