from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas

from db.database import get_db

from db import models

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=schemas.UserInDB)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await models.User.create(db, **user.model_dump())
    return schemas.UserInDB(**user.__dict__)


@router.get("/{identifier}", response_model=schemas.UserPublic)
async def get_user(identifier: str, db: AsyncSession = Depends(get_db)):
    user = await models.User.get(db, identifier)
    return schemas.UserPublic(**user.__dict__)


@router.get("/get-users", response_model=list[schemas.UserPublic])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await models.User.get_all(db)
    return [schemas.UserPublic(**user.__dict__) for user in users]
