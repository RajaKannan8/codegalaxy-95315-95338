from pydantic import BaseModel


# PUBLIC_INTERFACE
class Dispute(BaseModel):
    id: int
    title: str
    status: str
    raised_by: str


# PUBLIC_INTERFACE
class DisputeCreate(BaseModel):
    title: str
    details: str
