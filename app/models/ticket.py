from enum import StrEnum

from sqlalchemy import Column, DateTime, Enum, Integer, ForeignKey, func, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class PaidStatus(StrEnum):
    PAID = 'Оплачено'
    CANCELED = 'Отменено'
    BOOKED = 'Забронировано'


class Ticket(Base):
    number = Column(String)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    passenger_id = Column(Integer, ForeignKey('passenger.id'))
    created_at = Column(DateTime, server_default=func.now())
    paid_date = Column(DateTime)
    status = Column(Enum(PaidStatus), default=PaidStatus.BOOKED)
    flight = relationship(
        'Flight',
        back_populates='tickets',
        uselist=False,
        lazy='joined',
        foreign_keys=[flight_id]
    )
    passenger = relationship(
        'Passenger',
        back_populates='tickets',
        uselist=False,
        lazy='joined',
        foreign_keys=[passenger_id]
    )

    def __repr__(self):
        return f'{self.flight.number} {self.passenger.surname} {self.passenger.name[0]}'
