from fastapi import Request, FastAPI, logger
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.shared.exception.ai_model_not_defined_exception import CSException
from app.shared.exception.cs_http_exception import CSHTTPException
import logging

logger = logging.getLogger(__name__)

async def cs_exception_handler(request: Request, exc: CSException):
    return JSONResponse(
        status_code=400,
        content={"error": "Error", "message": exc.message},
    )

async def cs_http_exception_handler(request: Request, exc: CSHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500, 
        content={"error": "Internal Server Error", "message": "Something went wrong. Please try again later."},
    )

def init_exception_handlers(app: FastAPI):
    app.add_exception_handler(CSException, cs_exception_handler)
    app.add_exception_handler(CSHTTPException, cs_http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)