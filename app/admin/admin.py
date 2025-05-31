import contextlib
from datetime import datetime
from typing import Any, AsyncGenerator

from fastapi import HTTPException, Request
from sqladmin import ModelView
from wtforms import StringField, TelField
from wtforms.validators import Email, Length, Regexp, StopValidation

from app.core.db import get_async_session
from app.core.user import UserManager, get_user_db
from app.crud.user import user_crud
from app.models import (
    City,
    Discount,
    Flight,
    FlightCity,
    Passenger,
    RouteCost,
    Ticket,
    User,
)
from app.schemas.user import UserCreate


class PasswordSuperUserRequired:
    """Проверка пароля суперпользователя."""

    def __init__(self, message: str | None = None) -> None:
        """Инициализация валидатора пароля суперпользователя."""
        self.message = message
        self.field_flags = {'required': True}

    def __call__(self, form: Any, field: Any) -> None:
        """Валидация данных формы."""
        is_superuser = getattr(form, 'is_superuser').data

        if is_superuser and field.data == ' ':
            message = field.gettext('Для суперпользователя пароль обязятелен!')
        elif is_superuser is False and field.data != ' ':
            message = field.gettext('У обычного пользователя пароль - пробел!')
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)


class UsernameSuperUserRequired:
    """Проверка username суперпользователя."""

    def __init__(self, message: str | None = None) -> None:
        """Инициализация валидатора username."""
        self.message = message
        self.field_flags = {'required': False}

    def __call__(self, form: Any, field: Any) -> None:
        """Валидация данных формы."""
        is_superuser = getattr(form, 'is_superuser').data

        if is_superuser and field.data == ' ':
            message = field.gettext('Для суперпользователя username обязятелен!')
        elif is_superuser is False and field.data != ' ':
            message = field.gettext('Для обычного пользователя username не нужен!')
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)


class BirthdayValidator:

    def __init__(self, message: str | None = None) -> None:
        """Инициализация валидатора пароля суперпользователя."""
        self.message = message
        self.field_flags = {'required': True}

    def __call__(self, form, field):
        delta = datetime.now().year - field.data.year
        if delta < 15 or delta > 100:
            message = field.gettext('Возраст может быть от 15 до 100 лет!')
        else:
            message = self.message
        raise StopValidation(message)


class UserAdmin(ModelView, model=User):
    """Класс определяющий настройки админзоны модели User."""

    column_list = [
        'username',
        'name',
        'surname',
        'tg_username',
    ]
    # can_create = False
    # can_edit = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'
    column_labels = {'hashed_password': 'password'}
    column_details_list = [
        'username',
        'name',
        'surname',
        'tg_id',
        'tg_username',
        'birthday',
        'phone',
        'email',
        'is_active',
    ]
    form_create_rules = [
        'username',
        'name',
        'surname',
        'tg_id',
        'tg_username',
        'birthday',
        'phone',
        'email',
        'is_superuser',
        'hashed_password',
    ]
    form_edit_rules = [
        'name',
        'surname',
        'phone',
        'email',
        'birthday',
        'is_active',
    ]
    form_overrides = dict(
        hashed_password=StringField,
        phone=TelField,
    )
    form_args = dict(
        username=dict(
            default=None,
            validators=[
                UsernameSuperUserRequired(),
            ],
        ),
        birthday=dict(
            validators=[BirthdayValidator()],
        ),
        phone=dict(
            validators=[
                Length(
                    min=10,
                    max=15,
                    message='Телефон должен быть от 10 до 15 символов.',
                ),
                Regexp(
                    r'^\+?[0-9]+$',
                    message='Телефон должен содержать только цифры и символ '+'.',
                ),
            ],
        ),
        email=dict(
            validators=[Email()],
        ),
        hashed_password=dict(
            default=' ',
            validators=[PasswordSuperUserRequired()],
        ),
    )

    @contextlib.asynccontextmanager
    async def get_user_manager(self) -> AsyncGenerator[User, None]:
        """Генератор менеджера пользователей."""
        async for session in get_async_session():
            async for user_db in get_user_db(session):
                yield UserManager(user_db)

    async def on_model_change(
        self,
        data: dict,
        model: User,
        is_created: bool,
        request: Request,
    ) -> None:
        """Метод при изменении модели."""
        if is_created:
            unique_fields = [
                'username',
                'tg_id',
                'tg_username',
                'email',
            ]
            async for session in get_async_session():
                for field in unique_fields:
                    user = await user_crud.get_by_attribute(
                        attr_name=field,
                        attr_value=data[field],
                        session=session,
                    )
                    if user:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                f'Измените значение для поля {field}! '
                                'Такое значение уже есть.'
                            ),
                        )

            data['password'] = data['hashed_password']
            if data['password'] != ' ':
                data['password'] = data['password'].strip()
            if data['is_superuser'] is False:
                data['username'] = None

    async def after_model_change(
        self,
        data: dict,
        model: User,
        is_created: bool,
        request: Request,
    ) -> None:
        """Метод после изменении модели."""
        if is_created:
            async for session in get_async_session():
                user = await user_crud.get_by_attribute(
                    attr_name='email',
                    attr_value=data['email'],
                    session=session,
                )
            async with self.get_user_manager() as user_manager:
                await user_manager.update(UserCreate(**data), user)


class CityAdmin(ModelView, model=City):
    """Административный интерфейс для городов."""

    name = 'Город'
    name_plural = 'Города'
    icon = 'fa-solid fa-city'
    column_list = ['id', 'code', 'name']
    column_labels = {'id': 'ID', 'code': 'Код', 'name': 'Название'}


class FlightAdmin(ModelView, model=Flight):
    """Административный интерфейс для рейсов."""

    name = 'Рейс'
    name_plural = 'Рейсы'
    icon = 'fa-solid fa-plane'
    column_list = [
        'id',
        'number',
        'date_flight',
        'board',
        'status',
    ]
    column_labels = {
        'id': 'ID',
        'number': 'Номер',
        'date_flight': 'Дата',
        'board': 'Борт',
        'status': 'Статус',
    }


class PassengerAdmin(ModelView, model=Passenger):
    """Административный интерфейс для пассажиров."""

    name = 'Пассажир'
    name_plural = 'Пассажиры'
    icon = 'fa-solid fa-users'
    column_list = [
        'id',
        'name',
        'surname',
        'birthday',
        'doc_number',
        'phone',
        'email',
    ]
    column_labels = {
        'id': 'ID',
        'name': 'Имя',
        'surname': 'Фамилия',
        'birthday': 'Дата рождения',
        'doc_number': 'Номер документа',
        'phone': 'Телефон',
        'email': 'Email',
    }


class TicketAdmin(ModelView, model=Ticket):
    """Административный интерфейс для билетов."""

    name = 'Билет'
    name_plural = 'Билеты'
    icon = 'fa-solid fa-ticket'
    column_list = [
        'id',
        'number',
        'passenger_id',
        'flight_id',
        'status',
        'final_price',
        'created_at',
        'paid_date',
    ]
    column_labels = {
        'id': 'ID',
        'number': 'Номер',
        'passenger_id': 'Пассажир',
        'flight_id': 'Рейс',
        'status': 'Статус',
        'final_price': 'Цена',
        'created_at': 'Создан',
        'paid_date': 'Оплачен',
    }


class RouteCostAdmin(ModelView, model=RouteCost):
    """Административный интерфейс для стоимости маршрутов."""

    name = 'Стоимость маршрута'
    name_plural = 'Стоимость маршрутов'
    icon = 'fa-solid fa-money-bill'
    column_list = [
        'id',
        'from_city_id',
        'to_city_id',
        'cost',
    ]
    column_labels = {
        'id': 'ID',
        'from_city_id': 'Откуда',
        'to_city_id': 'Куда',
        'cost': 'Стоимость',
    }


class DiscountAdmin(ModelView, model=Discount):
    """Административный интерфейс для скидок."""

    name = 'Скидка'
    name_plural = 'Скидки'
    icon = 'fa-solid fa-percent'
    column_list = [
        'id',
        'code',
        'discount_percent',
        'is_active',
    ]
    column_labels = {
        'id': 'ID',
        'code': 'Код',
        'discount_percent': 'Процент',
        'is_active': 'Активна',
    }


class FlightCityAdmin(ModelView, model=FlightCity):
    """Административный интерфейс для городов в рейсах."""

    name = 'Город в рейсе'
    name_plural = 'Города в рейсах'
    icon = 'fa-solid fa-plane-arrival'
    column_list = [
        'id',
        'flight_id',
        'city_id',
        'order',
    ]
    column_labels = {
        'id': 'ID',
        'flight_id': 'Рейс',
        'city_id': 'Город',
        'order': 'Порядок',
    }
