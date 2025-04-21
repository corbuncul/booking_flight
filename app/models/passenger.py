from sqlalchemy import Column, Date, String

from app.core.db import Base

NAME_MAX_LENGHT = 100
PHONE_MAX_LENGHT = 15
DOC_MAX_LENGHT = 15


class Passenger(Base):
    name = Column(String(NAME_MAX_LENGHT))
    surname = Column(String(NAME_MAX_LENGHT))
    phone = Column(String(PHONE_MAX_LENGHT))
    email = Column(String(NAME_MAX_LENGHT))
    birthday = Column(Date)
    doc_number = Column(String(DOC_MAX_LENGHT))
    tg_id = Column(String)

    def __repr__(self):
        return f'{self.surname} {self.name[0]}'
