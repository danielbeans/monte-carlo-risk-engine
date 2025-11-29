import fastapi

router = fastapi.APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}
