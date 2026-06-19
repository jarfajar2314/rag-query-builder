from fastapi import APIRouter, HTTPException
from app.models.status_rule import StatusRuleCreate, StatusRuleUpdate
from app.services.status_rule_service import (
    create_status_rule,
    get_status_rules,
    get_status_rule,
    update_status_rule
)

router = APIRouter()

@router.post("")
def create_rule(rule: StatusRuleCreate):
    try:
        return create_status_rule(rule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
def list_rules():
    try:
        return get_status_rules()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{rule_id}")
def get_rule(rule_id: int):
    try:
        return get_status_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{rule_id}")
def update_rule(rule_id: int, updates: StatusRuleUpdate):
    try:
        return update_status_rule(rule_id, updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
