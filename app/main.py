import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.logging_config import configure_logging
from app.routers import tasks

configure_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("TaskFlow API started")
    try:
        yield
    finally:
        logger.info("TaskFlow API shutting down")
        
app = FastAPI(
    title=settings.app_name,
    description="A task management API built with Python.",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(tasks.router,prefix="/tasks")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error occurred")
    return JSONResponse(
        status_code=500,
        content={
            "detail":"Internal Server Error"
        }
    )
    


@app.get("/")
def read_root():
    return {
        "message":"Welcome to TaskFlow API"
    }

@app.get("/health")
def health_check():
    return{
        "status":"healthy"
    }









