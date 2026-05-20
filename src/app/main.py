from contextlib import asynccontextmanager

import sqlalchemy
import databases
from fastapi import FastAPI

from app.database import database, metadata, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    from models.transactions import accounts, transactions

    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

app = FastAPI(
    lifespan= lifespan,
    title= "Bank API",
    description= "API bancária assíncrona com FastAPI",
    version= "1.0.0",
)

from controllers import auth, transaction
app.include_router(auth.router)
app.include_router(transaction.router)