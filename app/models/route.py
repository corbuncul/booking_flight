from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base

ROUTE_MAX_LENGHT = 20


class Route(Base):

    from_city_id = Column(Integer, ForeignKey('city.id'))
    to_city_id = Column(Integer, ForeignKey('city.id'))
    cost = Column(Integer)
    from_city = relationship('City', foreign_keys=[from_city_id])
    to_city = relationship('City', foreign_keys=[to_city_id])

    def __repr__(self):
        return f'{self.from_city.name} -> {self.to_city.name}'
