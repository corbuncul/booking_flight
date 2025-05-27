from sqlalchemy import Column, Integer, ForeignKey

from app.core.db import Base


class FlightCity(Base):
    flight_id = Column(Integer, ForeignKey('flight.id'))
    city_id = Column(Integer, ForeignKey('city.id'))
