from fastapi import APIRouter
from ..models.bugs import Bug, BugCreate

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=list[Bug])
async def list_bugs():
    return []


# PUBLIC_INTERFACE
@router.post("/", response_model=Bug)
async def add_bug(bug: BugCreate):
    return Bug(id=1, title=bug.title, description=bug.description)
