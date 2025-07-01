from fastapi import APIRouter
from ..models.redeem import Reward, RewardRedeem

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/rewards", response_model=list[Reward])
async def list_rewards():
    return [Reward(id=1, name='Sticker', points=20)]


# PUBLIC_INTERFACE
@router.post("/redeem", response_model=RewardRedeem)
async def redeem_reward(reward: RewardRedeem):
    return RewardRedeem(
        user_id=reward.user_id,
        reward_id=reward.reward_id,
        status="pending",
    )
