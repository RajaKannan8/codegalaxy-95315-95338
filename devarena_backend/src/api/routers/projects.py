from fastapi import APIRouter
from ..models.projects import Project, ProjectCreate

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=list[Project])
async def list_projects():
    """Get all projects (stub)"""
    return [Project(id=1, name="Sample Project", description="Demo")]


# PUBLIC_INTERFACE
@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate):
    """Create new project (stub)"""
    return Project(id=2, name=project.name, description=project.description)
