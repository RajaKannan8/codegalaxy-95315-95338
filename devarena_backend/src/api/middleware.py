from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from starlette.responses import Response
from .models.auth import User, Role


MOCK_USERS = {
    "mock-jwt": User(
        id=1,
        username="admin",
        email="admin@demo.org",
        roles=[Role.ADMIN],
    ),
    "demo-jwt": User(
        id=10,
        username="user",
        email="user@demo.org",
        roles=[Role.DEVELOPER],
    ),
}


# PUBLIC_INTERFACE
class JWTBearer(HTTPBearer):
    """JWT Auth middleware for FastAPI routes, enforcing presence and validity of JWT."""

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if credentials:
            jwt_token = credentials.credentials
            if jwt_token in MOCK_USERS:
                # Store user in request state
                request.state.user = MOCK_USERS[jwt_token]
                return credentials
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# PUBLIC_INTERFACE
def get_current_user(request: Request) -> User:
    """Dependency for extracting current user from request.state."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user


# PUBLIC_INTERFACE
async def add_version_header(request: Request, call_next):
    """FastAPI middleware to add API version header."""
    response: Response = await call_next(request)
    response.headers["X-API-Version"] = "v1"
    return response
