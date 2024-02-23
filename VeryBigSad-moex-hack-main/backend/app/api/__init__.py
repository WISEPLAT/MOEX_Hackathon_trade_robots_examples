from fastapi import APIRouter
from api.v1 import router as router_v1
from api.auth.endpoints import router as auth_router

router = APIRouter()
router.include_router(router_v1, prefix="/v1", tags=["v1"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])


@router.get("/", tags=["api-health"])
async def health():
    return {"status": "ok"}
