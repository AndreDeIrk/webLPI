from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram = Column(String, unique=True, index=True)
    hashed_password = Column(String)
