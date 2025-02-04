from sqlalchemy import Column, Integer, String

from app.core.db import Base

ROUTE_MAX_LENGHT = 20


class Route(Base):
    from_town = Column(String(ROUTE_MAX_LENGHT))
    to_town = Column(String(ROUTE_MAX_LENGHT))
    cost = Column(Integer)

    def __repr__(self):
        return f'{self.from_town} {self.to_town}'
