from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class ErrorHandler:
    def __init__(self, app: FastAPI):
        @app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            logger.error(f"Global exception: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"message": "Internal server error", "detail": str(exc)}
            )

        @app.middleware("http")
        async def log_requests(request: Request, call_next: Callable):
            logger.info(f"Request path: {request.url.path}")
            try:
                response = await call_next(request)
                return response
            except Exception as e:
                logger.error(f"Request failed: {str(e)}", exc_info=True)
                raise
            