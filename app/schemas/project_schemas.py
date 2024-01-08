from datetime import date, datetime
from typing import List, Optional

from fastapi import Form
from pydantic import BaseModel

from app.schemas import RecordInDB, RecordReturn, RecordCreate


class Project(BaseModel):
    country: Optional[str] = None
    city: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    name: str
    owner_id: str


class ProjectStart(Project):
    records: List[RecordCreate] | None = Form(...)
    name: str = Form(...)
    owner_id: str = Form(...)


class ProjectInDB(Project):
    id: str
    created_at: datetime
    records: list[RecordInDB] = None


class ProjectReturn(ProjectInDB):
    records: list[RecordReturn] = None
