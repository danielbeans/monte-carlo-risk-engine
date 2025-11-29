"""FastAPI dependencies for dependency injection."""

from typing import Annotated

import fastapi

from mcengine.db import redis_rq


RedisRQServiceDep = Annotated[
    redis_rq.RedisRQService, fastapi.Depends(redis_rq.get_redis_rq_service)
]
