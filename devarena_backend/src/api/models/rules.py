from pydantic import BaseModel


# PUBLIC_INTERFACE
class Rule(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool


# PUBLIC_INTERFACE
class RuleCreate(BaseModel):
    name: str
    description: str
