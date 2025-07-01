from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ..models.rules import Rule, RuleCreate
from ..middleware import get_current_user
from .auth import require_roles, Role, User


router = APIRouter()

_RULES: Dict[int, Rule] = {}
_next_rule_id = 1


class ESLintIntegration:
    """Scaffold: Integration with ESLint/SonarQube."""

    def fetch_rules(self):
        pass


eslint_stub = ESLintIntegration()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[Rule], summary="List rules", tags=["Rules"])
async def list_rules(current_user: User = Depends(get_current_user)):
    """List all rules."""
    return list(_RULES.values())


# PUBLIC_INTERFACE
@router.post(
    "/",
    response_model=Rule,
    summary="Add a new rule",
    tags=["Rules"],
    responses={403: {"description": "Forbidden"}},
)
async def add_rule(
    rule: RuleCreate, current_user: User = Depends(get_current_user)
):
    """Add new rule (admin only)."""
    require_roles(current_user, [Role.ADMIN])
    global _next_rule_id
    new_rule = Rule(
        id=_next_rule_id,
        name=rule.name,
        description=rule.description,
        is_active=True
    )
    _RULES[_next_rule_id] = new_rule
    _next_rule_id += 1
    return new_rule


# PUBLIC_INTERFACE
@router.patch(
    "/{rule_id}/activate",
    response_model=Rule,
    summary="Activate rule",
    tags=["Rules"]
)
async def activate_rule(rule_id: int, current_user: User = Depends(get_current_user)):
    require_roles(current_user, [Role.ADMIN])
    if rule_id not in _RULES:
        raise HTTPException(status_code=404, detail="Rule not found")
    _RULES[rule_id].is_active = True
    return _RULES[rule_id]


# PUBLIC_INTERFACE
@router.patch(
    "/{rule_id}/deactivate",
    response_model=Rule,
    summary="Deactivate rule",
    tags=["Rules"]
)
async def deactivate_rule(rule_id: int, current_user: User = Depends(get_current_user)):
    require_roles(current_user, [Role.ADMIN])
    if rule_id not in _RULES:
        raise HTTPException(status_code=404, detail="Rule not found")
    _RULES[rule_id].is_active = False
    return _RULES[rule_id]


# PUBLIC_INTERFACE
@router.delete(
    "/{rule_id}",
    status_code=204,
    summary="Delete rule",
    tags=["Rules"]
)
async def delete_rule(rule_id: int, current_user: User = Depends(get_current_user)):
    require_roles(current_user, [Role.ADMIN])
    if rule_id not in _RULES:
        raise HTTPException(status_code=404, detail="Rule not found")
    del _RULES[rule_id]
    return None
