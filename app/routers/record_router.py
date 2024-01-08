from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from db import models
from db.database import get_db

router = APIRouter(prefix="/record", tags=["record"])


@router.post("/add")
async def add_record(
        data: schemas.RecordCreate, db: AsyncSession = Depends(get_db), ):
    result = await models.Record.create(db, **data.model_dump())
    return schemas.RecordReturn(**result.__dict__)
