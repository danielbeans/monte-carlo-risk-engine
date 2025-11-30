"""RQ tasks for commission simulation."""

import json
import redis
from typing import Any

from mcengine import config
from mcengine import services
from mcengine.db import postgres
from mcengine.db import redis_rq


def process_commission_simulation(job_id: str, request: dict[str, Any]) -> dict[str, Any]:
    result = services.commission.run_commission_simulation(request)

    redis_rq_service = redis_rq.RedisRQService()
    redis_rq_service.cache_result(job_id, json.dumps(result))
    
    postgres_service = postgres.PostgresService()
    postgres_service.save_result(job_id, json.dumps(result))
    
    return result