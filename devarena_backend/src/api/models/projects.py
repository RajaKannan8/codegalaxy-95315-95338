from pydantic import BaseModel


# PUBLIC_INTERFACE
class Project(BaseModel):
    id: int
    name: str
    description: str


# PUBLIC_INTERFACE
class ProjectCreate(BaseModel):
    name: str
    description: str
