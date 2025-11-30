import json
import uuid
from typing import Any

import fastapi

from mcengine import config
from mcengine import dependencies
from mcengine import schemas
from mcengine import tasks

router = fastapi.APIRouter(prefix="/commission")


@router.post(
    "/simulate",
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=schemas.commission.CommissionSimulationResponse,
)
async def enqueue_commission_simulation(
    request: schemas.commission.CommissionSimulationRequest,
    redis_rq_service: dependencies.RedisRQServiceDep,
) -> schemas.commission.CommissionSimulationResponse:
    job_id = str(uuid.uuid4())

    job = redis_rq_service.enqueue_task(
        tasks.commission.process_commission_simulation,
        job_id,
        request=request.model_dump(),
        queue_name=config.settings.commission_queue,
    )

    return {"job_id": job_id}


@router.get(
    "/results/{job_id}",
    response_model=dict[str, Any],
)
async def get_commission_simulation_result(
    job_id: str,
    redis_rq_service: dependencies.RedisRQServiceDep,
    postgres_service: dependencies.PostgresServiceDep,
) -> dict[str, Any]:
    # Try to get cached result first (this is the fastest path)
    cached_result = redis_rq_service.get_cached_result(job_id)
    if cached_result:
        print(f"Cached result found for job {job_id}")
        return json.loads(cached_result)

    postgres_result = postgres_service.get_result(job_id)
    if postgres_result:
        print(f"Result found in PostgreSQL for job {job_id}, caching in Redis")
        redis_rq_service.cache_result(job_id, json.dumps(postgres_result))
        return postgres_result

    # If not in PostgreSQL, check job status
    job = redis_rq_service.get_job(job_id)

    if job.is_finished:
        if job.result:
            # ! Theoretically, this should never happen
            result_dict = json.loads(job.result)
            redis_rq_service.cache_result(job_id, job.result)
            postgres_service.save_result(job_id, result_dict)
            return result_dict
        else:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} completed but no result available",
            )
    elif job.is_failed:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job {job_id} failed: {job.exc_info}",
        )
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_202_ACCEPTED,
            detail=f"Job {job_id} is still processing",
        )
