"""
FastAPI backend application initialization.
"""

from __future__ import annotations

import contextlib
from typing import AsyncGenerator

import fastapi
from fastapi.middleware import cors

from risk_engine.api import routes


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        title="Monte Carlo Risk Engine",
        description="Event-driven portfolio risk analysis API",
        version="0.1.0",
        lifespan=lifespan,
    )

    add_middleware(app)
    add_routers(app)

    return app


# Actions before and after the application begins accepting requests.
# See: https://fastapi.tiangolo.com/advanced/events/?h=#lifespan
@contextlib.asynccontextmanager
async def lifespan(_: fastapi.FastAPI) -> AsyncGenerator[None, None]:
    # Setup

    yield

    # Teardown
    pass


def add_middleware(app: fastapi.FastAPI) -> None:
    # TODO: Tighten this up
    origins = ["*"]
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_routers(app: fastapi.FastAPI) -> None:
    health_router = fastapi.APIRouter()
    health_router.get("/health")(lambda: {"status": "healthy"})
    app.include_router(health_router)

    app.include_router(routes.api_router, prefix="/api/v1")


app = create_app()


@app.exception_handler(Exception)
async def global_exception_handler(
    _: fastapi.Request, exc: Exception
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
