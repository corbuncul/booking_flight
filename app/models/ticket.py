from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    func,
    String,
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from app.core.constants import CODE_MAX_LENGHT, TICKET_MAX_LENGHT, TicketStatus
from app.core.db import Base
from app.models import City, Flight, Passenger


class Ticket(Base):
    number: Mapped[str] = mapped_column(
        String(TICKET_MAX_LENGHT), nullable=True
    )
    status: Mapped[TicketStatus] = mapped_column(default=TicketStatus.BOOKED)
    passenger_id: Mapped[int] = mapped_column(ForeignKey('passenger.id'))
    flight_id: Mapped[int] = mapped_column(ForeignKey('flight.id'))
    from_city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    to_city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    discount_code: Mapped[str] = mapped_column(
        String(CODE_MAX_LENGHT), nullable=True
    )
    final_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    paid_date: Mapped[datetime] = mapped_column(nullable=True)
    passenger: Mapped['Passenger'] = relationship(
        'Passenger', backref='tickets', lazy='joined'
    )
    flight: Mapped['Flight'] = relationship(
        'Flight', backref='tickets', lazy='joined'
    )
    from_city: Mapped['City'] = relationship(
        'City', foreign_keys=[from_city_id], lazy='joined'
    )
    to_city: Mapped['City'] = relationship(
        'City', foreign_keys=[to_city_id], lazy='joined'
    )

    def __repr__(self):
        return f'билет № {self.number} статус {self.status}'
