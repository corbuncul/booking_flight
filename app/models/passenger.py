from sqlalchemy import Column, Date, String

from app.core.constants import (
    DOC_MAX_LENGHT,
    NAME_MAX_LENGHT,
    PHONE_MAX_LENGHT,
)
from app.core.db import Base


class Passenger(Base):
    name = Column(String(NAME_MAX_LENGHT), nullable=False)
    surname = Column(String(NAME_MAX_LENGHT), nullable=False)
    phone = Column(String(PHONE_MAX_LENGHT), nullable=True)
    email = Column(String(NAME_MAX_LENGHT), nullable=True)
    birthday = Column(Date, nullable=False)
    doc_number = Column(String(DOC_MAX_LENGHT), nullable=False)
    tg_id = Column(String, nullable=True)

    def __repr__(self):
        return f'{self.surname} {self.name[0]}'
