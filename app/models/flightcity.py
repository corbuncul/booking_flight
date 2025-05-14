from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class FlightCity(Base):
    __tablename__ = 'flight_city'
    flight_id = Column(Integer, ForeignKey('flight.id'))
    city_id = Column(Integer, ForeignKey('city.id'))
    flight = relationship('Flight', back_populates='flight_cities')
    city = relationship('City', back_populates='city_flights')
