"""Entry point for running the FastAPI application."""

import uvicorn

from risk_engine import config


if __name__ == "__main__":
    uvicorn.run(
        "risk_engine.main:app",
        host=config.settings.api_host,
        port=config.settings.api_port,
        reload=config.settings.api_reload,
    )
