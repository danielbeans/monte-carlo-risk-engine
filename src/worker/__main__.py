import redis
import rq

from mcengine.config import settings

if __name__ == "__main__":
    queue_names = settings.queue_names
    print(f"Starting worker listening to queues: {queue_names}")

    worker = rq.Worker(
        queues=queue_names,
        connection=redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
        ),
    )
    worker.work()
