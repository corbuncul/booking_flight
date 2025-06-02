from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.db import Base


class RouteCost(Base):
    from_city_id = Column(Integer, ForeignKey('city.id'))
    to_city_id = Column(Integer, ForeignKey('city.id'))
    cost = Column(Float)
    from_city = relationship(
        'City',
        foreign_keys=[from_city_id],
        backref='outbound_routes',
        lazy='joined'
    )
    to_city = relationship(
        'City',
        foreign_keys=[to_city_id],
        backref='inbound_routes',
        lazy='joined'
    )

    def __repr__(self):
        return f'{self.from_city_id} -> {self.to_city_id}: {self.cost}'
