from fastapi import APIRouter, Depends
from typing import List, Dict
from ..models.gamification import Stats, Award, LeaderboardUser
from ..middleware import get_current_user
from .auth import User


router = APIRouter()

# In-memory gamification data
_USER_XP: Dict[int, int] = {1: 120, 2: 30}
_USER_AWARDS: Dict[int, List[Award]] = {
    1: [Award(id=1, name="First Commit", description="Awarded for first PR merged")]
}
_LEADERBOARD: List[LeaderboardUser] = [
    LeaderboardUser(user_id=1, username="admin", xp=120, level=3),
    LeaderboardUser(user_id=2, username="user", xp=30, level=1)
]


class GamificationIntegration:
    def announce_levelup(self, user_id: int, level: int):
        pass


gamification_stub = GamificationIntegration()


# PUBLIC_INTERFACE
@router.get("/stats", response_model=Stats, summary="Get my gamification stats", tags=["Gamification"])
async def get_stats(current_user: User = Depends(get_current_user)):
    xp = _USER_XP.get(current_user.id, 0)
    level = xp // 50 + 1
    rank = next(
        (i + 1 for i, lbu in enumerate(_LEADERBOARD)
         if lbu.user_id == current_user.id),
        len(_LEADERBOARD)
    )
    return Stats(xp=xp, level=level, rank=rank)


# PUBLIC_INTERFACE
@router.get("/awards", response_model=List[Award], summary="Get my awards/badges", tags=["Gamification"])
async def get_awards(current_user: User = Depends(get_current_user)):
    return _USER_AWARDS.get(current_user.id, [])


# PUBLIC_INTERFACE
@router.get(
    "/leaderboard",
    response_model=List[LeaderboardUser],
    summary="Get XP leaderboard",
    tags=["Gamification"]
)
async def get_leaderboard(current_user: User = Depends(get_current_user)):
    return sorted(_LEADERBOARD, key=lambda u: -u.xp)
