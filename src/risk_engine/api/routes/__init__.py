import fastapi

from risk_engine.api.routes import root

api_router = fastapi.APIRouter()
api_router.include_router(root.router, prefix="/api/v1")
