from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer

from app.core.db import Base


class Queue(Base):
    passenger = Column(Integer, ForeignKey('passenger.id'))
    flight = Column(Integer, ForeignKey('flight.id'))
    create_date = Column(Date, default=date.today)

    def __repr__(self):
        return f'{self.passenger} {self.flight} {self.create_date}'
