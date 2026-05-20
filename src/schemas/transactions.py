from datetime import datetime
from pydantic import BaseModel

class TransactionIn(BaseModel):
    account_id: int
    type: str  # ou será deposit ou withdraw
    amount: float

class TransactionUpdateIn(BaseModel):
    type: str | None = None
    amount: float | None = None