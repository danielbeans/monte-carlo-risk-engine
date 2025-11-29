from typing import Any, Callable

import redis
import rq

from mcengine.config import settings


class RedisRQService:
    """Service for interacting with Redis Queue (RQ) and result caching."""

    def __init__(self) -> None:
        self._redis_client: redis.Redis | None = None
        self._queue: rq.Queue | None = None

    def get_redis_client(self) -> redis.Redis:
        if self._redis_client is None:
            self._redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
            )
        return self._redis_client

    def get_queue(self) -> rq.Queue:
        if self._queue is None:
            redis_client = self.get_redis_client()
            self._queue = rq.Queue(
                name=settings.task_queue_key, connection=redis_client
            )
        return self._queue

    def enqueue_task(self, func: Callable, *args: Any, **kwargs: Any) -> rq.job.Job:
        queue = self.get_queue()
        return queue.enqueue(func, *args, **kwargs)

    def get_job_status(self, job_id: str) -> str | None:
        redis_client = self.get_redis_client()
        job = rq.job.Job.fetch(job_id, connection=redis_client)
        return job.get_status()

    def get_job_result(self, job_id: str) -> Any | None:
        redis_client = self.get_redis_client()
        job = rq.job.Job.fetch(job_id, connection=redis_client)
        if job.is_finished:
            return job.result
        return None

    def get_job(self, job_id: str) -> rq.job.Job | None:
        redis_client = self.get_redis_client()
        return rq.job.Job.fetch(job_id, connection=redis_client)

    def get_all_jobs(self) -> list[rq.job.Job]:
        queue = self.get_queue()
        return queue.jobs

    def cache_result(self, task_id: str, result_json: str) -> None:
        redis_client = self.get_redis_client()
        key = f"{settings.result_cache_prefix}{task_id}"
        redis_client.setex(key, settings.cache_ttl_seconds)

    def get_cached_result(self, task_id: str) -> str | None:
        redis_client = self.get_redis_client()
        key = f"{settings.result_cache_prefix}{task_id}"
        result = redis_client.get(key)
        return result.decode("utf-8") if result else None

    def close(self) -> None:
        if self._redis_client is not None:
            self._redis_client.close()
            self._redis_client = None
            self._queue = None


REDIS_RQ_SERVICE = RedisRQService()


async def get_redis_rq_service() -> RedisRQService:
    return REDIS_RQ_SERVICE
