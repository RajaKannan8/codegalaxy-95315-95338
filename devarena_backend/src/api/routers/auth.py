from fastapi import APIRouter, Depends, HTTPException
from ..models.auth import LoginRequest, LoginResponse, UserCreate, Role, User
from ..middleware import get_current_user
from typing import Dict


router = APIRouter()


_auth_users: Dict[str, User] = {
    "admin": User(id=1, username="admin", email="admin@demo.org", roles=[Role.ADMIN]),
    "user": User(id=2, username="user", email="user@demo.org", roles=[Role.DEVELOPER]),
}
_auth_passwords: Dict[str, str] = {
    "admin": "test",
    "user": "demo"
}
_next_user_id = 3


def _find_user_by_username(username: str) -> User:
    user = _auth_users.get(username)
    return user


# PUBLIC_INTERFACE
@router.post(
    "/login",
    summary="User login",
    response_model=LoginResponse,
    tags=["Authentication"],
    responses={401: {"description": "Invalid credentials"}},
)
async def login(req: LoginRequest):
    """
    Authenticate a user with username and password.

    Returns access token and user details on success.
    """
    if req.username in _auth_passwords and _auth_passwords[req.username] == req.password:
        user = _auth_users[req.username]
        # Use username as dummy JWT token for demo
        return LoginResponse(
            access_token=f"{user.username}-jwt",
            token_type="bearer",
            user=user,
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")


# PUBLIC_INTERFACE
@router.post(
    "/register",
    summary="User registration",
    response_model=User,
    tags=["Authentication"],
)
async def register(user: UserCreate):
    """
    Register a new user.

    Returns the created user (roles: developer by default).
    """
    global _next_user_id
    if user.username in _auth_users:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(
        id=_next_user_id,
        username=user.username,
        email=user.email,
        roles=[Role.DEVELOPER],
    )
    _auth_users[user.username] = new_user
    _auth_passwords[user.username] = user.password
    _next_user_id += 1
    return new_user


# PUBLIC_INTERFACE
@router.get(
    "/me",
    summary="Get current logged-in user",
    response_model=User,
    tags=["Authentication"],
)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns the authenticated user.
    """
    return current_user


# Utility for RBAC elsewhere
def require_roles(user: User, required_roles: list[Role]):
    if not set(user.roles).intersection(set(required_roles)):
        raise HTTPException(status_code=403, detail="Forbidden: Insufficient role")
