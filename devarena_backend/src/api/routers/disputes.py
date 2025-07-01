from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ..models.disputes import Dispute, DisputeCreate
from ..middleware import get_current_user
from .auth import require_roles, Role, User


router = APIRouter()

_DISPUTES: Dict[int, Dispute] = {}
_next_dispute_id = 1


class DisputeResolutionIntegration:
    def escalate(self, dispute: Dispute):
        pass

    def notify_moderator(self, dispute: Dispute):
        pass


resolution_stub = DisputeResolutionIntegration()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[Dispute], summary="List all disputes", tags=["Disputes"])
async def list_disputes(current_user: User = Depends(get_current_user)):
    return list(_DISPUTES.values())


# PUBLIC_INTERFACE
@router.post("/", response_model=Dispute, summary="Create new dispute", tags=["Disputes"])
async def add_dispute(dispute: DisputeCreate, current_user: User = Depends(get_current_user)):
    """Any user can raise a dispute."""
    global _next_dispute_id
    new = Dispute(
        id=_next_dispute_id,
        title=dispute.title,
        status="pending",
        raised_by=current_user.username,
    )
    _DISPUTES[_next_dispute_id] = new
    _next_dispute_id += 1
    # resolution_stub.notify_moderator(new)
    return new


# PUBLIC_INTERFACE
@router.patch(
    "/{dispute_id}/resolve",
    response_model=Dispute,
    summary="Resolve dispute",
    tags=["Disputes"],
    responses={403: {"description": "Forbidden"}},
)
async def resolve_dispute(dispute_id: int, current_user: User = Depends(get_current_user)):
    require_roles(current_user, [Role.ADMIN])
    dispute = _DISPUTES.get(dispute_id)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    dispute.status = "resolved"
    return dispute


# PUBLIC_INTERFACE
@router.delete(
    "/{dispute_id}",
    status_code=204,
    summary="Delete dispute",
    tags=["Disputes"],
    responses={403: {"description": "Forbidden"}},
)
async def delete_dispute(dispute_id: int, current_user: User = Depends(get_current_user)):
    require_roles(current_user, [Role.ADMIN])
    if dispute_id not in _DISPUTES:
        raise HTTPException(status_code=404, detail="Dispute not found")
    del _DISPUTES[dispute_id]
    return None
