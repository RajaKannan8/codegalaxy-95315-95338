from fastapi import APIRouter
from ..models.rules import Rule, RuleCreate

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=list[Rule])
async def list_rules():
    """List rules (stub)"""
    return []


# PUBLIC_INTERFACE
@router.post("/", response_model=Rule)
async def add_rule(rule: RuleCreate):
    """Add new rule (stub)"""
    return Rule(
        id=1,
        name=rule.name,
        description=rule.description,
        is_active=True,
    )
