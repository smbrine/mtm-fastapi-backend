from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from db import models
from db.database import get_db

router = APIRouter(prefix="/photo", tags=["photo"])


@router.post("/add")
async def add_photo(
        data: schemas.PhotoAdd = Depends(), db: AsyncSession = Depends(get_db), ):
    photo_data = await data.object.read()
    result = await models.Photo.create(
        db, object=photo_data, **data.model_dump(exclude=["object", "identifier"])
    )
    return schemas.PhotoReturn(**result.__dict__)
