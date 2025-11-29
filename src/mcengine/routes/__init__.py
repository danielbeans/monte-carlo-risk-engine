import fastapi

from mcengine.routes import commission, core

api_router = fastapi.APIRouter()
api_router.include_router(core.router)
api_router.include_router(commission.router)
