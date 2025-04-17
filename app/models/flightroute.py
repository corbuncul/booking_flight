from sqlalchemy import Column, DateTime, Integer, ForeignKey

from app.core.db import Base


class FlightRoute(Base):

    flight_id = Column(Integer, ForeignKey('flight.id'))
    route_id = Column(Integer, ForeignKey('route.id'))
    route_order = Column(Integer)
    datetime_out = Column(DateTime)
    datetime_in = Column(DateTime)
