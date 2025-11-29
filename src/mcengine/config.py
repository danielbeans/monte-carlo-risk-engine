import os

import dotenv
import pydantic_settings

dotenv.load_dotenv()


class Settings(pydantic_settings.BaseSettings):
    # API Settings
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = os.getenv("API_PORT", 8000)
    api_reload: bool = os.getenv("API_RELOAD", False)

    # Redis Settings
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_db: int = os.getenv("REDIS_DB", 0)
    redis_password: str | None = os.getenv("REDIS_PASSWORD", None)

    # PostgreSQL Settings
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = os.getenv("POSTGRES_PORT", 5432)
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_db: str = os.getenv("POSTGRES_DB", "mcengine")

    # Redis RQ Settings
    result_cache_prefix: str = os.getenv("RESULT_CACHE_PREFIX", "mcengine:result:")
    cache_ttl_seconds: int = os.getenv("CACHE_TTL_SECONDS", 600)  # 10 minutes
    _queue_names_str: str = os.getenv("QUEUE_NAMES", "default:queue")

    @property
    def queue_names(self) -> list[str]:
        queues = [q.strip() for q in self._queue_names_str.split(",") if q.strip()]
        return queues if queues else ["default:queue"]

    @property
    def default_queue(self) -> str:
        return self.queue_names[0]

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
