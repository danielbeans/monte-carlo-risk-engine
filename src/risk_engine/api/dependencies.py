"""FastAPI dependencies for dependency injection."""

from typing import Annotated

import fastapi

from risk_engine.db import redis_rq


RedisServiceDep = Annotated[
    redis_rq.RedisRQService, fastapi.Depends(redis_rq.get_redis_rq_service)
]
