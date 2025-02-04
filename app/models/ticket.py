from sqlalchemy import Column, Integer, ForeignKey

from app.core.db import Base


class Ticket(Base):
    number = Column(Integer)
    flight = Column(Integer, ForeignKey('flight.id'))
    passenger = Column(Integer, ForeignKey('passenger.id'))

    def __repr__(self):
        return f'{self.number} {self.flight} {self.passenger}'
