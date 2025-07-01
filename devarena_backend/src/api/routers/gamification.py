from fastapi import APIRouter
from ..models.gamification import Stats, Award, LeaderboardUser

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/stats", response_model=Stats)
async def get_stats():
    return Stats(xp=100, level=2, rank=10)


# PUBLIC_INTERFACE
@router.get("/awards", response_model=list[Award])
async def get_awards():
    return []


# PUBLIC_INTERFACE
@router.get("/leaderboard", response_model=list[LeaderboardUser])
async def get_leaderboard():
    return []
