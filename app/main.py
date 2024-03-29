from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import settings
from app.routers import photo_router, project_router, record_router, user_router
from db.database import sessionmanager

sessionmanager.init(settings.DATABASE_URL)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=[""],
)

v1 = APIRouter(prefix="/v1")

v1.include_router(user_router)
v1.include_router(photo_router)
v1.include_router(record_router)
v1.include_router(project_router)

app.include_router(v1)


@app.get("/")
async def root():
    return {"message": "alive!"}


if __name__ == "__main__":
    print(settings.SSL_CERT_PATH, settings.SSL_KEY_PATH)
    if settings.IS_HTTPS:
        uvicorn.run(
            "app.main:app",
            host=settings.SERVER_BIND_HOSTNAME,
            port=int(settings.SERVER_BIND_PORT),
            reload=True,
            ssl_certfile=settings.SSL_CERT_PATH,
            ssl_keyfile=settings.SSL_KEY_PATH,
        )
    else:
        uvicorn.run(
            "app.main:app",
            host=settings.SERVER_BIND_HOSTNAME,
            port=int(settings.SERVER_BIND_PORT),
            reload=True,
        )
