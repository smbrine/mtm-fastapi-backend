from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import settings
from app.routers import photo_router, record_router, user_router
from db.database import sessionmanager

sessionmanager.init(settings.DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=[""]
)

v1 = APIRouter(prefix="/v1")

v1.include_router(user_router)
v1.include_router(photo_router)
v1.include_router(record_router)

app.include_router(v1)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)
