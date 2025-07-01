from fastapi import APIRouter
from ..models.disputes import Dispute, DisputeCreate

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=list[Dispute])
async def list_disputes():
    return []


# PUBLIC_INTERFACE
@router.post("/", response_model=Dispute)
async def add_dispute(dispute: DisputeCreate):
    return Dispute(id=1, title=dispute.title, status="pending", raised_by="user1")
