from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ..models.projects import Project, ProjectCreate
from ..middleware import get_current_user
from .auth import require_roles, Role, User


router = APIRouter()

_PROJECTS: Dict[int, Project] = {
    1: Project(id=1, name="Sample Project", description="Demo"),
}
_next_project_id = 2


class VCSIntegration:
    """Scaffold: VCS integration (GitHub/GitLab/Bitbucket)."""

    def create_repo(self, name, description):
        pass

    def sync(self, project_id):
        pass


vcs_stub = VCSIntegration()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[Project], summary="List all projects", tags=["Projects"])
async def list_projects(current_user: User = Depends(get_current_user)):
    """Get all projects."""
    # RBAC: any authenticated user
    return list(_PROJECTS.values())


# PUBLIC_INTERFACE
@router.post(
    "/",
    response_model=Project,
    summary="Create new project",
    tags=["Projects"],
    responses={403: {"description": "Forbidden"}},
)
async def create_project(
    project: ProjectCreate, current_user: User = Depends(get_current_user)
):
    """Create new project (admin/reviewer only)."""
    require_roles(current_user, [Role.ADMIN, Role.REVIEWER])
    global _next_project_id
    proj = Project(
        id=_next_project_id,
        name=project.name,
        description=project.description
    )
    _PROJECTS[_next_project_id] = proj
    _next_project_id += 1
    # Could trigger vcs_stub.create_repo
    return proj


# PUBLIC_INTERFACE
@router.get(
    "/{project_id}",
    response_model=Project,
    summary="Get project details",
    tags=["Projects"]
)
async def get_project(project_id: int, current_user: User = Depends(get_current_user)):
    proj = _PROJECTS.get(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


# PUBLIC_INTERFACE
@router.delete(
    "/{project_id}",
    status_code=204,
    summary="Delete a project",
    tags=["Projects"]
)
async def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    require_roles(current_user, [Role.ADMIN])
    if project_id not in _PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")
    del _PROJECTS[project_id]
    return None
