from fastapi import APIRouter
from ..models.gamification import LeaderboardUser

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=list[LeaderboardUser])
async def get_leaderboard():
    return []
