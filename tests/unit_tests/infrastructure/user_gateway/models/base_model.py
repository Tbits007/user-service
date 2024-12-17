from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )