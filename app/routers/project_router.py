from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from db import models
from db.database import get_db

router = APIRouter(prefix="/project", tags=["project"])


@router.post("/start")
async def start_project(
    data: schemas.ProjectStart = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await models.Project.create(db, **data.model_dump())
    return schemas.ProjectReturn(**result.__dict__)
