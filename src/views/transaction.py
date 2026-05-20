from datetime import datetime
from pydantic import BaseModel

class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    created_at: datetime