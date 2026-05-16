from datetime import datetime

from sqlalchemy import ForeignKey, Float, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(String)

    amount: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id")
    )

    account = relationship(
        "Account",
        back_populates="transactions"
    )