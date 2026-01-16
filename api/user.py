from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from database.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user: dict, db: Session = Depends(get_db)):
    trader = User(
        name=user["name"],
        whatsapp_number=user["whatsapp_number"],
        account_balance=user["account_balance"],
        risk_percent=user.get("risk_percent", 1.0),
        min_lot=user.get("min_lot", 0.001),
        max_lot=user.get("max_lot", 1.0),
        receive_signals=user.get("receive_signals", True),
        receive_high_profit_only=user.get("high_profit_only", False)
    )

    db.add(trader)
    db.commit()
    db.refresh(trader)

    return {"status": "registered", "user_id": trader.id}
