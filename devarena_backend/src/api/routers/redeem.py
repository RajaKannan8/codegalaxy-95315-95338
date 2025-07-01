from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ..models.redeem import Reward, RewardRedeem
from ..middleware import get_current_user
from .auth import User  # Fix F821

router = APIRouter()

_REWARDS: Dict[int, Reward] = {
    1: Reward(id=1, name="Sticker", points=20),
    2: Reward(id=2, name="T-shirt", points=100),
}
_USER_REDEMPTIONS: List[RewardRedeem] = []


class RewardIntegration:
    def fulfill(self, user_id: int, reward_id: int):
        pass


reward_stub = RewardIntegration()


# PUBLIC_INTERFACE
@router.get(
    "/rewards",
    response_model=List[Reward],
    summary="List redeemable rewards",
    tags=["Redeem"]
)
async def list_rewards(current_user: User = Depends(get_current_user)):
    return list(_REWARDS.values())


# PUBLIC_INTERFACE
@router.post(
    "/redeem",
    response_model=RewardRedeem,
    summary="Redeem a reward",
    tags=["Redeem"]
)
async def redeem_reward(
    reward: RewardRedeem, current_user: User = Depends(get_current_user)
):
    """Redeem a reward if enough points."""
    if reward.reward_id not in _REWARDS:
        raise HTTPException(status_code=404, detail="Reward not found")
    record = RewardRedeem(
        user_id=current_user.id, reward_id=reward.reward_id, status="pending"
    )
    _USER_REDEMPTIONS.append(record)
    # reward_stub.fulfill(...)
    return record


# PUBLIC_INTERFACE
@router.get(
    "/my-redemptions",
    response_model=List[RewardRedeem],
    summary="My redemption history",
    tags=["Redeem"]
)
async def get_my_redemptions(current_user: User = Depends(get_current_user)):
    return [r for r in _USER_REDEMPTIONS if r.user_id == current_user.id]
