from sqlalchemy import Column, String

from app.core.db import Base


class City(Base):
    name = Column(String)
    code = Column(String)

    def __repr__(self):
        return f'{self.name}'
