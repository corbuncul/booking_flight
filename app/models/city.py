from sqlalchemy import Column, String

from app.core.db import Base


class City(Base):
    name = Column(String, unique=True)
    code = Column(String, unique=True)

    def __repr__(self):
        return f'{self.name}'
