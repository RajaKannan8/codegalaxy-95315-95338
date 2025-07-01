from fastapi import APIRouter, Depends, HTTPException
from ..models.auth import LoginRequest, LoginResponse, UserCreate, Role, User
from ..middleware import get_current_user

router = APIRouter()


# PUBLIC_INTERFACE
@router.post("/login", summary="User login", response_model=LoginResponse)
async def login(req: LoginRequest):
    # Placeholder for authentication logic
    if req.username == "admin" and req.password == "test":
        return LoginResponse(
            access_token="mock-jwt",
            token_type="bearer",
            user=User(
                id=1,
                username="admin",
                email="admin@demo.org",
                roles=[Role.ADMIN],
            ),
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")


# PUBLIC_INTERFACE
@router.post("/register", summary="User registration", response_model=User)
async def register(user: UserCreate):
    # Placeholder: Return user details
    return User(
        id=2,
        username=user.username,
        email=user.email,
        roles=[Role.DEVELOPER],
    )


# PUBLIC_INTERFACE
@router.get("/me", summary="Get current logged-in user", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    # Returns mock user
    return current_user
