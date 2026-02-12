"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import phase1, phase2, phase3, cleanup
from app.core.config import settings
from app.core.logging import LoggerSetup

# Initialize logging
LoggerSetup.setup()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.

    Handles startup and shutdown events.
    """
    # Startup
    settings.ensure_directories()
    yield
    # Shutdown (if needed)


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade FastAPI service for vulnerability report automation",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(phase1.router, prefix="/api")
app.include_router(phase2.router, prefix="/api")
app.include_router(phase3.router, prefix="/api")
app.include_router(cleanup.router, prefix="/api/cleanup", tags=["Cleanup"])


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": "Vulnerability Report Automation Service",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """
    Global health check endpoint.

    Returns:
        Service status
    """
    return {"status": "healthy", "service": "vulnerability-report-automation"}


@app.get("/info")
async def info() -> dict[str, Any]:
    """
    Service information endpoint.

    Returns:
        Service configuration and status
    """
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "max_file_size_mb": settings.max_file_size_mb,
        "endpoints": {
            "phase1_parse": "/api/phase1/parse",
            "phase2_generate": "/api/phase2/generate",
            "phase3_generate": "/api/phase3/generate",
            "cache_info": "/api/cleanup/cache-info",
            "purge_cache": "/api/cleanup/purge-cache",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
