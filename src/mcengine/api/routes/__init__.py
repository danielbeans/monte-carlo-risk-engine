import fastapi

from mcengine.api.routes import commission, root

api_router = fastapi.APIRouter()
api_router.include_router(root.router)
api_router.include_router(commission.router)
