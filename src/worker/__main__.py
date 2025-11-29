import redis
import rq

from mcengine.config import settings

if __name__ == "__main__":
    worker = rq.Worker(
        queues=[settings.task_queue_key],
        connection=redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
        ),
    )
    worker.work()
