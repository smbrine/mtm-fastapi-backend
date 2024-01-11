import io

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response, StreamingResponse

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
    data: schemas.PhotoAdd = Depends(),
    db: AsyncSession = Depends(get_db),
):
    extension = data.object.filename.split(".")[-1]
    photo_data = await data.object.read()
    result = await models.Photo.create(
        db,
        object=photo_data,
        extension=extension,
        **data.model_dump(exclude=["object", "identifier"]),
    )
    return schemas.PhotoReturn(**result.__dict__)


@router.get("/s")
async def get_photos(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 5):
    photos = await models.Photo.get_all(db, skip=skip, limit=limit)
    return [schemas.PhotoReturn(**photo.__dict__) for photo in photos]


@router.get("/{filename}")
async def get_photo(filename: str, db: AsyncSession = Depends(get_db)):
    identifier, extension = filename.split(".")
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
