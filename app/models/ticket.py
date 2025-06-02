from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    ForeignKey,
    Float,
    func,
    String,
)
from sqlalchemy.orm import relationship

from app.core.constants import CODE_MAX_LENGHT, TICKET_MAX_LENGHT, TicketStatus
from app.core.db import Base


class Ticket(Base):
    number = Column(String(TICKET_MAX_LENGHT), nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.BOOKED)
    passenger_id = Column(Integer, ForeignKey('passenger.id'))
    flight_id = Column(Integer, ForeignKey('flight.id'))
    from_city_id = Column(Integer, ForeignKey('city.id'))
    to_city_id = Column(Integer, ForeignKey('city.id'))
    discount_code = Column(String(CODE_MAX_LENGHT), nullable=True)
    final_price = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    paid_date = Column(DateTime, nullable=True)
    passenger = relationship('Passenger', backref='tickets', lazy='joined')
    flight = relationship('Flight', backref='tickets', lazy='joined')
    from_city = relationship(
        'City', foreign_keys=[from_city_id], lazy='joined'
    )
    to_city = relationship(
        'City', foreign_keys=[to_city_id], lazy='joined'
    )

    def __repr__(self):
        return f'билет № {self.number} статус {self.status}'
