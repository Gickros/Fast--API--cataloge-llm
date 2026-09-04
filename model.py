import uuid
from decimal import Decimal

from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class Books(Base):
    __tablename__ = 'Books'
    title: Mapped[str]
    author: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric=(10, 2))
    description: Mapped[str | None] = mapped_column(nullable=True, default=None)
    genre: Mapped[str | None] = mapped_column(nullable=True, default=None)
