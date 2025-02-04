from sqlalchemy import Column, Date, String

from app.core.db import Base

NAME_MAX_LENGHT = 100
PHONE_MAX_LENGHT = 15
DOC_MAX_LENGHT = 15


class Passenger(Base):
    first_name = Column(String(NAME_MAX_LENGHT))
    surname = Column(String(NAME_MAX_LENGHT))
    last_name = Column(String(NAME_MAX_LENGHT))
    phone = Column(String(PHONE_MAX_LENGHT))
    email = Column(String(NAME_MAX_LENGHT))
    date_of_birth = Column(Date)
    doc_number = Column(String(DOC_MAX_LENGHT))

    def __repr__(self):
        return f'{self.first_name} {self.surname[0]} {self.last_name[0]}'
