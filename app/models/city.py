from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.constants import CODE_MAX_LENGHT, NAME_MAX_LENGHT
from app.core.db import Base


class City(Base):
    code = Column(String(CODE_MAX_LENGHT), unique=True, index=True)
    name = Column(String(NAME_MAX_LENGHT))
    flights = relationship(
        'Flight',
        secondary='flight_city',
        back_populates='cities',
        lazy='joined'
    )

    def __repr__(self):
        return f'{self.name}'
