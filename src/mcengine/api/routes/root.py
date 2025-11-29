import fastapi

from mcengine.api.dependencies import RedisServiceDep
from mcengine.services.tasks import test_task

router = fastapi.APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/test", response_model=dict[str, str])
async def test(redis_service: RedisServiceDep) -> dict[str, str]:
    job = redis_service.enqueue_task(test_task, "test")
    return {"message": "Hello, World", "job_id": job.id}


@router.get("/test1")
async def test1(redis_service: RedisServiceDep):
    jobs = redis_service.get_all_jobs()
    return {"message": "Hello, World", "jobs": [job.result for job in jobs]}
