import sqlalchemy
from app.database import metadata

accounts = sqlalchemy.Table(
    "accounts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key= True),
    sqlalchemy.Column("owner", sqlalchemy.String(100), nullable= False),
    sqlalchemy.Column("balance", sqlalchemy.Float, default= 0.0, nullable= False),

)

transactions = sqlalchemy.Table(
    "transactions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key= True),
    sqlalchemy.Column("account_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("accounts.id"), nullable= False),
    sqlalchemy.Column("type", sqlalchemy.String(10), nullable= False), # se será deposit ou withdraw
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable= False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable= False),
)