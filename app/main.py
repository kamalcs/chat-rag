from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router

from app.api.documents import router as documents_router

from app.core.config import settings

from app.core.dependencies import vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    yield

    # Shutdown
    vector_store.close()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)


app.include_router(chat_router)

app.include_router(documents_router)


@app.get("/")
async def root():

    return {
        "message": (f"{settings.app_name} " "API is running"),
        "version": (settings.app_version),
    }
