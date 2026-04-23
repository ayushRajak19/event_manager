"""
FastAPI main application factory.
Initialize and configure the FastAPI app with all routes, middleware, and startup events.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import init_db
from app.api import api_router


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Create FastAPI instance
    app = FastAPI(
        title=settings.APP_NAME,
        description="Technical Event Management System - API Documentation",
        version=settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )

    # Add CORS middleware for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Initialize database on startup
    @app.on_event("startup")
    async def startup_event():
        """Initialize database tables on application startup."""
        init_db()
        print(f"✓ {settings.APP_NAME} started successfully")
        print(f"✓ Database initialized")
        print(f"✓ API Documentation available at http://localhost:8000/api/docs")

    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        """
        Health check endpoint.
        
        Returns:
            dict: Health status
        """
        return {
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION
        }

    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """
        Root endpoint - API information.
        
        Returns:
            dict: API information and available endpoints
        """
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "api_docs": "http://localhost:8000/api/docs",
            "redoc": "http://localhost:8000/api/redoc"
        }

    # Include all API routes
    app.include_router(api_router)

    return app


# Create the application instance
app = create_app()
