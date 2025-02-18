from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings
from app.api.routes import cs0a0100001
from app.api.routes import cs0a0100002

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(cs0a0100001.router, prefix="/files", tags=["files"])
api_router.include_router(cs0a0100002.router, prefix="/cs0a0100002", tags=["conversation_message"])


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
