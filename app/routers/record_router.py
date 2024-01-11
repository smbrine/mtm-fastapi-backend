from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import schemas
from db import models
from db.database import get_db

router = APIRouter(prefix="/record", tags=["record"])


async def convert_to_geojson(objs: Iterable):
    feature_collection = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:4326",
            },
        },
        "features": [],
    }
    for _obj in objs:
        obj_dict = _obj.__dict__
        feature = {
            "type": "Feature",
            "properties": obj_dict,
            "geometry": {
                "coordinates": [
                    obj_dict.get("longitude"),
                    obj_dict.get("latitude"),
                ],
                "type": "Point",
            },
        }
        feature_collection["features"].append(feature)
    return feature_collection


@router.post("/add")
async def add_record(
    data: schemas.RecordCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await models.Record.create(db, **data.model_dump())
    return schemas.RecordReturn(**result.__dict__)


@router.get("/s")
async def get_all_records(
    project_id: str = None,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
):
    if project_id:
        project = await db.get(models.Project, project_id, options=[selectinload(models.Project.records)])
        if not project:
            return {"error": "Project not found"}
        records = project.records
    else:
        stmt = select(models.Record).offset(skip).limit(limit)
        result = await db.execute(stmt)
        records = result.scalars().all()

    return [schemas.RecordReturn(**record.__dict__) for record in records]


@router.get("/s/geojson")
async def get_all_records(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 20
):
    records = await models.Record.get_all(db, skip=skip, limit=limit)

    return await convert_to_geojson(records)
