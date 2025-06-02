from sqlalchemy import Column, Enum, Date, String, Time
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
    date_flight = Column(Date, nullable=False)
    time_flight = Column(Time, nullable=False)
    status = Column(Enum(FlightStatus))
    cities = relationship(
        'City',
        secondary='flight_city',
        back_populates='flights',
        lazy='joined'
    )

    def __repr__(self):
        return f'{self.number} {self.date_flight}'
