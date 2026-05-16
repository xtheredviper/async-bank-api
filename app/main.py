from fastapi import FastAPI

from app.core.database import engine, Base

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction

from app.routers.auth import router as auth_router

from app.routers.transactions import router as transaction_router


app = FastAPI(
    title="Bank API"
)

app.include_router(auth_router)

app.include_router(transaction_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Bank API running"}