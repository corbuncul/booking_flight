import re

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from sqlalchemy import func, or_
from sqlalchemy.orm import Query
from sqlalchemy.sql.selectable import Select

from app.models import User


class UserFilter(Filter):
    """Класс фильтрации пользователей по фамилии и имени."""

    full_name: str | None = Field(None)

    class Constants(Filter.Constants):  # noqa: D106
        model = User
        search_field_name = 'full_name'

    def filter(self, query: Query | Select) -> Query | Select:
        """Функция настройки фильтра."""
        if self.full_name:
            full_name = re.sub(r'\s{2,}', ' ', self.full_name).strip()
            full_name_variant1 = func.concat(
                User.name, ' ', User.surname
            )
            full_name_variant2 = func.concat(
                User.surname, ' ', User.name
            )
            query = query.where(
                or_(
                    full_name_variant1.ilike(f'%{full_name}%'),
                    full_name_variant2.ilike(f'%{full_name}%'),
                ),
            )
        return query
