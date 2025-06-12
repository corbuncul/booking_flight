from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models import City


class RouteCost(Base):
    from_city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    to_city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    cost: Mapped[float]
    from_city: Mapped[list['City']] = relationship(
        'City',
        foreign_keys=[from_city_id],
        backref='outbound_routes',
        lazy='joined'
    )
    to_city: Mapped[list['City']] = relationship(
        'City',
        foreign_keys=[to_city_id],
        backref='inbound_routes',
        lazy='joined'
    )

    def __repr__(self):
        return f'{self.from_city_id} -> {self.to_city_id}: {self.cost}'
