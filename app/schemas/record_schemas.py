from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import PhotoInDB


class Record(BaseModel):
    name: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    date: date
    project_id: str


class RecordCreate(Record):
    pass


class RecordInDB(Record):
    id: str
    created_at: date
    photos: Optional[list[PhotoInDB]] = None


class RecordReturn(RecordInDB):
    photos: Optional[list[str]] = None
