from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    LargeBinary,
    String,
    select,
)
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from db.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())

    @classmethod
    async def create(cls, db: AsyncSession, identifier=None, created_at=None, **kwargs):
        if not identifier:
            identifier = str(uuid4())
        if not created_at:
            created_at = datetime.now()

        transaction = cls(id=identifier, created_at=created_at, **kwargs)
        try:
            db.add(transaction)
            await db.commit()
            await db.refresh(transaction)
        except IntegrityError:
            await db.rollback()
            return None
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, identifier: str):
        try:
            transaction = await db.get(cls, identifier)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100):
        stmt = select(cls).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()


class User(BaseModel):
    __tablename__ = "users"
    first_name = Column(String)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationship to projects
    projects = relationship("Project", back_populates="owner")


class Project(BaseModel):
    __tablename__ = "projects"
    name = Column(String, nullable=False)
    country = Column(String)
    city = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    # User relationship
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")

    # Records relationship
    records = relationship("Record", back_populates="project", cascade="all, delete")


class Record(BaseModel):
    __tablename__ = "records"
    name = Column(String, nullable=False)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    date = Column(DateTime, default=datetime.now)

    # Project relationship
    project_id = Column(String, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="records")

    # Photos relationship
    photos = relationship(
        "Photo", back_populates="parent_record", cascade="all, delete"
    )


class Photo(BaseModel):
    __tablename__ = "photos"
    object = Column(LargeBinary)
    description = Column(String)
    date_taken = Column(DateTime, default=datetime.now)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Record relationship
    record_id = Column(String, ForeignKey("records.id"))
    parent_record = relationship("Record", back_populates="photos")
