from sqlalchemy import Column, Enum, DateTime, String
from sqlalchemy.orm import relationship

from app.core.constants import (
    BOARD_MAX_LENGHT,
    FLIGHT_MAX_LENGHT,
    FlightStatus,
)
from app.core.db import Base


class Flight(Base):
    number = Column(String(FLIGHT_MAX_LENGHT))
    board = Column(String(BOARD_MAX_LENGHT), nullable=True)
    date_flight = Column(DateTime, nullable=False)
    status = Column(Enum(FlightStatus))
    cities = relationship(
        'City', secondary='flight_city', back_populates='flights'
    )

    def __repr__(self):
        return f'{self.number} {self.date_flight}'
