import json
from datetime import date, datetime
from typing import Annotated, Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from app.schemas.utils import as_form


class Photo(BaseModel):
    description: str = "No description"
    latitude: Optional[float]
    longitude: Optional[float]
    record_id: str


class PhotoAdd(Photo):
    record_id: str = "uuid-for-record"
    description: str = "No description"
    latitude: float = 0.0
    longitude: float = 0.0

    date_taken: date = date.today()


@as_form
class PhotoAddForm(Photo):
    record_id: str = "uuid-for-record"
    description: str = "No description"
    latitude: float = 0.0
    longitude: float = 0.0

    date_taken: date = date.today()
    # @classmethod
    # def __get_validators__(cls):
    #     yield cls.validate_to_json
    #
    # @classmethod
    # def validate_to_json(cls, value):
    #     if isinstance(value, str):
    #         return cls(**json.loads(value))
    #     return value


class PhotoPublic(Photo):
    link: str
    date_taken: date
    owner_id: str


class PhotoReturn(Photo):
    id: str
    created_at: datetime
    date_taken: date
    owner_id: str

    extension: Optional[str] = None

    class ConfigDict:
        from_attributes = True


class PhotoInDB(Photo):
    id: str
    created_at: datetime
    object: bytes
    date_taken: date
    extension: str
    owner_id: str

    class ConfigDict:
        from_attributes = True
