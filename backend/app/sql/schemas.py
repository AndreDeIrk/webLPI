from typing import List, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    telegram: str


class UserCreate(UserBase):
    password: str


class Setting(BaseModel):
    id: int

    class Config:
        orm_mode: True


class User(UserBase):
    id: int
    items: List[Setting] = []

    class Config:
        orm_mode = True
