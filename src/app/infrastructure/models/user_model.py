import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.app.infrastructure.models.base_model import Base


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(
        "uuid",
        sa.Uuid,
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)