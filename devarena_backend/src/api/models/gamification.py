from pydantic import BaseModel


# PUBLIC_INTERFACE
class XPEvent(BaseModel):
    id: int
    user_id: int
    event: str
    xp: int


# PUBLIC_INTERFACE
class Stats(BaseModel):
    xp: int
    level: int
    rank: int


# PUBLIC_INTERFACE
class Award(BaseModel):
    id: int
    name: str
    description: str


# PUBLIC_INTERFACE
class LeaderboardUser(BaseModel):
    user_id: int
    username: str
    xp: int
    level: int
