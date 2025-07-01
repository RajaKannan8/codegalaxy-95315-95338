"""
Main entry point for DevArena Backend API.
- Sets up FastAPI app with CORS, versioning, exception handling, and routes for all core modules.
- Provides JWT-based authentication/role-based access control middleware for route protection.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import (
    auth,
    projects,
    rules,
    bugs,
    disputes,
    gamification,
    redeem,
    leaderboards,
    notifications,
)
from .middleware import JWTBearer, add_version_header

API_VERSION = "v1"

app = FastAPI(
    title="DevArena Backend API",
    description="Backend for DevArena: Centralized, Gamified PR Review Platform.",
    version=API_VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(add_version_header)

# Exception handler for all uncaught errors
@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    # Optionally log the error here!
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )


# E302: Ensure TWO blank lines above function
@app.get("/", tags=["Health"])
async def health_check():
    """
    PUBLIC_INTERFACE: Health check endpoint.
    Returns status if the server is healthy.
    """
    return {"message": "Healthy", "version": API_VERSION}


# Versioned API root
API_PREFIX = f"/api/{API_VERSION}"

# Include all routers, with JWT required for most endpoints except auth
app.include_router(
    auth.router, prefix=f"{API_PREFIX}/auth", tags=["Authentication"]
)
app.include_router(
    projects.router,
    prefix=f"{API_PREFIX}/projects",
    tags=["Projects"],
    dependencies=[JWTBearer()],
)
app.include_router(
    rules.router,
    prefix=f"{API_PREFIX}/rules",
    tags=["Rules"],
    dependencies=[JWTBearer()],
)
app.include_router(
    bugs.router,
    prefix=f"{API_PREFIX}/bugs",
    tags=["Bugs"],
    dependencies=[JWTBearer()],
)
app.include_router(
    disputes.router,
    prefix=f"{API_PREFIX}/disputes",
    tags=["Disputes"],
    dependencies=[JWTBearer()],
)
app.include_router(
    gamification.router,
    prefix=f"{API_PREFIX}/gamification",
    tags=["Gamification"],
    dependencies=[JWTBearer()],
)
app.include_router(
    redeem.router,
    prefix=f"{API_PREFIX}/redeem",
    tags=["Redeem"],
    dependencies=[JWTBearer()],
)
app.include_router(
    leaderboards.router,
    prefix=f"{API_PREFIX}/leaderboards",
    tags=["Leaderboards"],
    dependencies=[JWTBearer()],
)
app.include_router(
    notifications.router,
    prefix=f"{API_PREFIX}/notifications",
    tags=["Notifications"],
    dependencies=[JWTBearer()],
)
