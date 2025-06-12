from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.core.constants import CODE_MAX_LENGHT
from app.core.db import Base


class Discount(Base):
    code: Mapped[str] = mapped_column(
        String(CODE_MAX_LENGHT), unique=True, index=True
    )
    discount_percent: Mapped[float]
    is_active: Mapped[bool] = mapped_column(default=True)
