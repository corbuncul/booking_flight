from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from app.core.db import Base

BOARD_MAX_LENGHT = 10
FLIGHT_MAX_LENGHT = 10


class Flight(Base):
    number = Column(String(FLIGHT_MAX_LENGHT), nullable=False)
    board_number = Column(String(BOARD_MAX_LENGHT), nullable=True)
    date_flight = Column(DateTime, nullable=False)
    routes = relationship(
        'Route',
        secondary='FlightRoute',
        back_populates='flights'
    )

    def __repr__(self):
        return f'{self.number} {self.date_flight}'
