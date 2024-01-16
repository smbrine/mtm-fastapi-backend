import io
from json import JSONDecodeError

from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile
from pydantic import Json
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response, StreamingResponse
from typing import Annotated, Optional
import json

from app import schemas
from db import models
from db.database import get_db

router = APIRouter(prefix="/photo", tags=["photo"])


class RawResponse(Response):
    media_type = "binary/octet-stream"

    def render(self, content: bytes) -> bytes:
        return bytes([b ^ 0x54 for b in content])


@router.post("/add")
async def add_photo(
    data: schemas.PhotoAdd = Depends(schemas.PhotoAddForm),
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    photo_data = photo.file.read()
    extension = photo.filename.split(".")[-1]

    # Create the photo instance and add it to the database
    result = await models.Photo.create(
        db,
        object=photo_data,
        extension=extension,
        owner_id="uuid-for-user",
        **data.model_dump(exclude=["object", "identifier"]),
    )

    return schemas.PhotoReturn(**result.__dict__)


@router.get("/s")
async def get_photos(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 5):
    photos = await models.Photo.get_all(db, skip=skip, limit=limit)
    return [schemas.PhotoReturn(**photo.__dict__) for photo in photos]


@router.get("/{filename}")
async def get_photo(filename: str, db: AsyncSession = Depends(get_db)):
    identifier, _ = filename.split(".")
    photo = await models.Photo.get(db, identifier)
    result = photo.object

    image_stream = io.BytesIO(result)

    if photo.extension:
        img_type = photo.extension
        filename = f"{photo.id}.{photo.extension}"
    else:
        img_type = "jpg"
        filename = f"{photo.id}.jpg"

    # Set 'inline' to display image in the browser
    headers = {"Content-Disposition": f"inline; filename={filename}"}

    return StreamingResponse(
        content=image_stream, media_type=f"image/{img_type}", headers=headers
    )
