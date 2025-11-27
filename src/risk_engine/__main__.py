"""Entry point for running the FastAPI application."""

import uvicorn

from risk_engine.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
