from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.constants import (
    DOC_MAX_LENGHT,
    NAME_MAX_LENGHT,
    PHONE_MAX_LENGHT,
)
from app.core.db import Base


class Passenger(Base):
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGHT))
    surname: Mapped[str] = mapped_column(String(NAME_MAX_LENGHT))
    phone: Mapped[str] = mapped_column(String(PHONE_MAX_LENGHT), nullable=True)
    email: Mapped[str] = mapped_column(String(NAME_MAX_LENGHT), nullable=True)
    birthday: Mapped[date]
    doc_number: Mapped[str] = mapped_column(String(DOC_MAX_LENGHT))
    tg_id: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f'{self.surname} {self.name[0]}'
