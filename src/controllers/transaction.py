from typing import Annotated

from fastapi import APIRouter, Depends, status

from core.security import login_required
from schemas.transaction import TransactionIn
from services.transaction import TransactionService
from views.transaction import TransactionOut, AccountOut


router = APIRouter(prefix="/transactions", tags=["Transactions"])

service = TransactionService()


@router.get("/balance/{account_id}", response_model=AccountOut)
async def get_balance(
    account_id: int,
    current_user: Annotated[dict, Depends(login_required)]
):
    return await service.get_balance(account_id)


@router.post("/deposit", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
async def deposit(
    data: TransactionIn,
    current_user: Annotated[dict, Depends(login_required)]
):
    return await service.deposit(data)


@router.post("/withdraw", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
async def withdraw(
    data: TransactionIn,
    current_user: Annotated[dict, Depends(login_required)]
):
    return await service.withdraw(data)


@router.get("/statement/{account_id}", response_model=list[TransactionOut])
async def get_statement(
    account_id: int,
    current_user: Annotated[dict, Depends(login_required)]
):
    return await service.get_statement(account_id)