from fastapi import APIRouter, Depends
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


@router.get("/s")
async def get_projects(db: AsyncSession = Depends(get_db)):
    projects = await models.Project.get_all(db)
    return [schemas.ProjectReturn(**project.__dict__) for project in projects]
