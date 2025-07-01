from pydantic import BaseModel


# PUBLIC_INTERFACE
class Bug(BaseModel):
    id: int
    title: str
    description: str


# PUBLIC_INTERFACE
class BugCreate(BaseModel):
    title: str
    description: str

