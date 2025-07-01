from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ..models.bugs import Bug, BugCreate
from ..middleware import get_current_user
from .auth import require_roles, Role, User


router = APIRouter()

_BUGS: Dict[int, Bug] = {}
_next_bug_id = 1


class BugTrackerIntegration:
    def file_issue(self, bug: Bug):
        pass


tracker_stub = BugTrackerIntegration()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[Bug], summary="List logged bugs", tags=["Bugs"])
async def list_bugs(current_user: User = Depends(get_current_user)):
    return list(_BUGS.values())


# PUBLIC_INTERFACE
@router.post("/", response_model=Bug, summary="Log new bug", tags=["Bugs"])
async def add_bug(bug: BugCreate, current_user: User = Depends(get_current_user)):
    """Log a new bug (any authenticated user)."""
    global _next_bug_id
    new_bug = Bug(id=_next_bug_id, title=bug.title, description=bug.description)
    _BUGS[_next_bug_id] = new_bug
    _next_bug_id += 1
    # Could trigger: tracker_stub.file_issue(new_bug)
    return new_bug


# PUBLIC_INTERFACE
@router.delete(
    "/{bug_id}",
    status_code=204,
    summary="Delete a bug",
    tags=["Bugs"],
    responses={403: {"description": "Forbidden"}},
)
async def delete_bug(bug_id: int, current_user: User = Depends(get_current_user)):
    require_roles(current_user, [Role.ADMIN, Role.REVIEWER])
    if bug_id not in _BUGS:
        raise HTTPException(status_code=404, detail="Bug not found")
    del _BUGS[bug_id]
    return None
