from fastapi import APIRouter, Depends
from typing import List
from ..models.gamification import LeaderboardUser
from ..middleware import get_current_user
from .auth import User


router = APIRouter()

_LEADERBOARD: List[LeaderboardUser] = [
    LeaderboardUser(user_id=1, username="admin", xp=120, level=3),
    LeaderboardUser(user_id=2, username="user", xp=30, level=1)
]


# PUBLIC_INTERFACE
@router.get(
    "/",
    response_model=List[LeaderboardUser],
    summary="XP Leaderboard",
    tags=["Leaderboards"]
)
async def get_leaderboard(current_user: User = Depends(get_current_user)):
    return sorted(_LEADERBOARD, key=lambda u: -u.xp)
