from sqlalchemy import Column, DateTime, Integer, ForeignKey, String

from app.core.db import Base

BOARD_MAX_LENGHT = 10
FLIGHT_MAX_LENGHT = 10


class Flight(Base):
    number = Column(String(FLIGHT_MAX_LENGHT))
    board_number = Column(String(BOARD_MAX_LENGHT))
    route = Column(Integer, ForeignKey('route.id'))
    date_flight = Column(DateTime)

    def __repr__(self):
        return f'{self.number} {self.route} {self.date_flight}'
