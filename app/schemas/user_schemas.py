from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserCreate(User):
    password: str


class UserLogin(User):
    password: str


class UserPublic(User):
    first_name: str


class UserInDB(User):
    id: str
    created_at: datetime
    first_name: str
    password: str
    is_active: bool
    is_superuser: bool
