from sqlalchemy import Column, String, Float, Boolean

from app.core.constants import CODE_MAX_LENGHT
from app.core.db import Base


class Discount(Base):
    code = Column(String(CODE_MAX_LENGHT), unique=True, index=True)
    discount_percent = Column(Float)
    is_active = Column(Boolean, default=True)
