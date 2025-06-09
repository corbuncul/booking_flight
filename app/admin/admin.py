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

        if is_superuser and field.data == '':
            message = field.gettext('Для суперпользователя пароль обязятелен!')
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

        if is_superuser and field.data == '':
            message = field.gettext('Для суперпользователя username обязятелен!')
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
        User.id,
        User.username,
        User.name,
        User.surname,
        User.tg_username,
    ]
    # can_create = False
    # can_edit = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'
    column_labels = {
        User.id: 'ID',
        User.username: 'Ник',
        User.name: 'Имя',
        User.surname: 'Фамилия',
        User.tg_username: 'Ник в телеграм',
        User.hashed_password: 'Пароль'
    }
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
    column_list = [City.id, City.code, City.name]
    column_labels = {City.id: 'ID', City.code: 'Код', City.name: 'Название'}


class FlightAdmin(ModelView, model=Flight):
    """Административный интерфейс для рейсов."""

    name = 'Рейс'
    name_plural = 'Рейсы'
    icon = 'fa-solid fa-plane'
    column_list = [
        Flight.id,
        Flight.number,
        Flight.date_flight,
        Flight.board,
        Flight.status,
    ]
    column_labels = {
        Flight.id: 'ID',
        Flight.number: 'Номер',
        Flight.date_flight: 'Дата',
        Flight.board: 'Борт',
        Flight.status: 'Статус',
    }


class PassengerAdmin(ModelView, model=Passenger):
    """Административный интерфейс для пассажиров."""

    name = 'Пассажир'
    name_plural = 'Пассажиры'
    icon = 'fa-solid fa-users'
    column_list = [
        Passenger.id,
        Passenger.name,
        Passenger.surname,
        Passenger.birthday,
        Passenger.doc_number,
        Passenger.phone,
        Passenger.email,
    ]
    column_labels = {
        Passenger.id: 'ID',
        Passenger.name: 'Имя',
        Passenger.surname: 'Фамилия',
        Passenger.birthday: 'Дата рождения',
        Passenger.doc_number: 'Номер документа',
        Passenger.phone: 'Телефон',
        Passenger.email: 'Email',
    }


class TicketAdmin(ModelView, model=Ticket):
    """Административный интерфейс для билетов."""

    name = 'Билет'
    name_plural = 'Билеты'
    icon = 'fa-solid fa-ticket'
    column_list = [
        Ticket.id,
        Ticket.number,
        Ticket.passenger_id,
        Ticket.flight_id,
        Ticket.status,
        Ticket.final_price,
        Ticket.created_at,
        Ticket.paid_date,
    ]
    column_labels = {
        Ticket.id: 'ID',
        Ticket.number: 'Номер',
        Ticket.passenger_id: 'Пассажир',
        Ticket.flight_id: 'Рейс',
        Ticket.status: 'Статус',
        Ticket.final_price: 'Цена',
        Ticket.created_at: 'Создан',
        Ticket.paid_date: 'Оплачен',
    }


class RouteCostAdmin(ModelView, model=RouteCost):
    """Административный интерфейс для стоимости маршрутов."""

    name = 'Стоимость маршрута'
    name_plural = 'Стоимость маршрутов'
    icon = 'fa-solid fa-money-bill'
    column_list = [
        RouteCost.id,
        RouteCost.from_city_id,
        RouteCost.to_city_id,
        RouteCost.cost,
    ]
    column_labels = {
        RouteCost.id: 'ID',
        RouteCost.from_city_id: 'Откуда',
        RouteCost.to_city_id: 'Куда',
        RouteCost.cost: 'Стоимость',
    }


class DiscountAdmin(ModelView, model=Discount):
    """Административный интерфейс для скидок."""

    name = 'Скидка'
    name_plural = 'Скидки'
    icon = 'fa-solid fa-percent'
    column_list = [
        Discount.id,
        Discount.code,
        Discount.discount_percent,
        Discount.is_active,
    ]
    column_labels = {
        Discount.id: 'ID',
        Discount.code: 'Код',
        Discount.discount_percent: 'Процент',
        Discount.is_active: 'Активна',
    }


class FlightCityAdmin(ModelView, model=FlightCity):
    """Административный интерфейс для городов в рейсах."""

    name = 'Город в рейсе'
    name_plural = 'Города в рейсах'
    icon = 'fa-solid fa-plane-arrival'
    column_list = [
        FlightCity.id,
        FlightCity.flight_id,
        FlightCity.city_id,
        FlightCity.order,
    ]
    column_labels = {
        FlightCity.id: 'ID',
        FlightCity.flight_id: 'Рейс',
        FlightCity.city_id: 'Город',
        FlightCity.order: 'Порядок',
    }
