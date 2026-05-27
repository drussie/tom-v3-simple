from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.api.config import settings
from apps.api.db import init_database
from apps.api.routers import (
    annotations,
    artifacts,
    dev,
    media,
    observations,
    pose,
    registry,
    replay,
    runs,
    tracklets,
    viewer,
)


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        if settings.create_db_on_startup:
            init_database()
        yield

    app = FastAPI(
        title="TOM v3 Simple API",
        version="0.0.0",
        description="Observation-only backend foundation for TOM v3 Simple.",
        lifespan=lifespan,
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(media.router)
    app.include_router(runs.router)
    app.include_router(registry.router)
    app.include_router(observations.router)
    app.include_router(artifacts.router)
    app.include_router(annotations.router)
    app.include_router(dev.router)
    app.include_router(tracklets.router)
    app.include_router(pose.router)
    app.include_router(replay.router)
    app.include_router(viewer.router)
    return app


app = create_app()
