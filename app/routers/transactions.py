from fastapi import APIRouter, Depends, HTTPException

from jose import jwt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.models.account import Account
from app.models.transaction import Transaction

from app.schemas.transaction import TransactionCreate


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/deposit")
async def deposit(
    transaction_data: TransactionCreate,
    token: str,
    db: AsyncSession = Depends(get_db)
):

    payload = jwt.decode(
        token,
        "supersecretkey",
        algorithms=["HS256"]
    )

    user_id = int(payload.get("sub"))

    if transaction_data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive"
        )

    result = await db.execute(
        select(Account).where(
            Account.owner_id == user_id
        )
    )

    account = result.scalar_one()

    account.balance += transaction_data.amount

    transaction = Transaction(
        type="deposit",
        amount=transaction_data.amount,
        account_id=account.id
    )

    db.add(transaction)

    await db.commit()

    return {
        "message": "Deposit successful",
        "balance": account.balance
    }


@router.post("/withdraw")
async def withdraw(
    transaction_data: TransactionCreate,
    token: str,
    db: AsyncSession = Depends(get_db)
):

    payload = jwt.decode(
        token,
        "supersecretkey",
        algorithms=["HS256"]
    )

    user_id = int(payload.get("sub"))

    if transaction_data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive"
        )

    result = await db.execute(
        select(Account).where(
            Account.owner_id == user_id
        )
    )

    account = result.scalar_one()

    if account.balance < transaction_data.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    account.balance -= transaction_data.amount

    transaction = Transaction(
        type="withdraw",
        amount=transaction_data.amount,
        account_id=account.id
    )

    db.add(transaction)

    await db.commit()

    return {
        "message": "Withdraw successful",
        "balance": account.balance
    }


@router.get("/statement")
async def statement(
    token: str,
    db: AsyncSession = Depends(get_db)
):

    payload = jwt.decode(
        token,
        "supersecretkey",
        algorithms=["HS256"]
    )

    user_id = int(payload.get("sub"))

    result = await db.execute(
        select(Account).where(
            Account.owner_id == user_id
        )
    )

    account = result.scalar_one()

    transactions_result = await db.execute(
        select(Transaction).where(
            Transaction.account_id == account.id
        )
    )

    transactions = transactions_result.scalars().all()

    return [
        {
            "type": transaction.type,
            "amount": transaction.amount
        }
        for transaction in transactions
    ]