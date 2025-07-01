from pydantic import BaseModel


# PUBLIC_INTERFACE
class Reward(BaseModel):
    id: int
    name: str
    points: int


# PUBLIC_INTERFACE
class RewardRedeem(BaseModel):
    user_id: int
    reward_id: int
    status: str
