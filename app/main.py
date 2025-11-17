from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routers.health import router as health_router
from app.api.routers.extract import router as extract_router
from app.api.routers.metrics import router as metrics_router
from app.core.logging import configure_logging
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    print("Starting AI service with env:", settings.ENV)
    yield


app = FastAPI(
    title="AI Service Demo",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router, prefix="")
app.include_router(extract_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")