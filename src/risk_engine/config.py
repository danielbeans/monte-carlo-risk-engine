import os
from typing import Optional

import dotenv
import pydantic_settings

dotenv.load_dotenv()


class Settings(pydantic_settings.BaseSettings):
    # API Settings
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = os.getenv("API_PORT", 8000)
    api_reload: bool = os.getenv("API_RELOAD", False)

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
