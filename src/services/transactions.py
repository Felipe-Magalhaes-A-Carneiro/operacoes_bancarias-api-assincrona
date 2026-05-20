from datetime import datetime

from databases.interfaces import Record
from fastapi import HTTPException, status

from app.database import database
from models.transactions import accounts, transactions
from schemas.transactions import TransactionIn


class TransactionService:
    async def get_balance(self, account_id: int) -> Record:
        return await self.__get_account_by_id(account_id)
    
    async def deposit(self, data: TransactionIn) -> Record:
        if data.amount <= 0:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail = "Deposit amount mus be positive."
            )
        
    
        accounts = await self.__get_account_by_id(data.account_id)

        # Atualização do saldo
        new_balance = accounts.balance + data.amount
        await database.execute(
            accounts.update()
            .where(accounts.c.id == data.account_id)
            .values(balance = new_balance)

        )

        # Registra transação
        await database.execute(
            transactions.insert().values(
                accounts_id = data.account_id,
                type = "deposit",
                amount = data.amount,
                created_at = datetime.now(),
            )
        )

        return await self.__get_account_by_id(data.account_id)
    
    async def withdraw(self, data: TransactionIn) -> Record:
        if data.amount <= 0:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Widraw amount must be positive."
            )
        
        accounts = await self.__get_account_by_id(data.account_id)

        if accounts.balance < data.amount:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Insufficient balance."
            )
        

        # Atualiza saldo
        new_balance = accounts.balance - data.amount
        await database.execute(
            accounts.update()
            .where(accounts.c.id == data.account_id)
            .values(balance = new_balance)
        )

        # Registra transação
        await database.execute(
            transactions.inser().values(
                accounts_id = data.account_id,
                type = "withdraw",
                amount = data.amount,
                created_at = datetime.now(),

            )
        )

        return await self.__get_account_by_id(data.account_id)
    
    async def get_statement(self, account_id: int) -> list[Record]:
        await self.__get_account_by_id(account_id)
        query = transactions.select().where(transactions.c.account_id == account_id)
        return await database.fetch_all(query)
    
    async def __get_account_by_id(self, account_id: int) -> Record:
        query = accounts.select().where(accounts.c.id == account_id)
        result = await database.fetch_one(query)
        if not result:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "Account not found."
            )
        return result