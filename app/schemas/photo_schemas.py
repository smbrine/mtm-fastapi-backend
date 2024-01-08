from datetime import date, datetime
from typing import Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class Photo(BaseModel):
    description: str = "No description"
    latitude: Optional[float]
    longitude: Optional[float]
    record_id: str


class PhotoAdd(Photo):
    object: UploadFile = File(...)
    record_id: str = Form(...)
    description: str = Form("No description")
    latitude: Optional[float] = Form(...)
    longitude: Optional[float] = Form(...)

    date_taken: date = Form(...)


class PhotoPublic(Photo):
    link: str
    date_taken: date


class PhotoReturn(Photo):
    id: str
    created_at: datetime
    date_taken: date

    class Config:
        from_attributes = True


class PhotoInDB(Photo):
    id: str
    created_at: datetime
    object: bytes
    date_taken: date

    class Config:
        from_attributes = True
