from sqladmin import ModelView

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


class CityAdmin(ModelView, model=City):
    """Административный интерфейс для городов."""

    name = "Город"
    name_plural = "Города"
    icon = "fa-solid fa-city"
    column_list = [City.id, City.code, City.name]
    column_labels = {City.id: "ID", City.code: "Код", City.name: "Название"}


class FlightAdmin(ModelView, model=Flight):
    """Административный интерфейс для рейсов."""

    name = "Рейс"
    name_plural = "Рейсы"
    icon = "fa-solid fa-plane"
    column_list = [
        Flight.id,
        Flight.number,
        Flight.date_flight,
        Flight.board,
        Flight.status,
    ]
    column_labels = {
        Flight.id: "ID",
        Flight.number: "Номер",
        Flight.date_flight: "Дата",
        Flight.board: "Борт",
        Flight.status: "Статус",
    }


class PassengerAdmin(ModelView, model=Passenger):
    """Административный интерфейс для пассажиров."""

    name = "Пассажир"
    name_plural = "Пассажиры"
    icon = "fa-solid fa-users"
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
        Passenger.id: "ID",
        Passenger.name: "Имя",
        Passenger.surname: "Фамилия",
        Passenger.birthday: "Дата рождения",
        Passenger.doc_number: "Номер документа",
        Passenger.phone: "Телефон",
        Passenger.email: "Email",
    }


class TicketAdmin(ModelView, model=Ticket):
    """Административный интерфейс для билетов."""

    name = "Билет"
    name_plural = "Билеты"
    icon = "fa-solid fa-ticket"
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
        Ticket.id: "ID",
        Ticket.number: "Номер",
        Ticket.passenger_id: "Пассажир",
        Ticket.flight_id: "Рейс",
        Ticket.status: "Статус",
        Ticket.final_price: "Цена",
        Ticket.created_at: "Создан",
        Ticket.paid_date: "Оплачен",
    }


class RouteCostAdmin(ModelView, model=RouteCost):
    """Административный интерфейс для стоимости маршрутов."""

    name = "Стоимость маршрута"
    name_plural = "Стоимость маршрутов"
    icon = "fa-solid fa-money-bill"
    column_list = [
        RouteCost.id,
        RouteCost.from_city_id,
        RouteCost.to_city_id,
        RouteCost.cost,
    ]
    column_labels = {
        RouteCost.id: "ID",
        RouteCost.from_city_id: "Откуда",
        RouteCost.to_city_id: "Куда",
        RouteCost.cost: "Стоимость",
    }


class DiscountAdmin(ModelView, model=Discount):
    """Административный интерфейс для скидок."""

    name = "Скидка"
    name_plural = "Скидки"
    icon = "fa-solid fa-percent"
    column_list = [
        Discount.id,
        Discount.code,
        Discount.discount_percent,
        Discount.is_active,
    ]
    column_labels = {
        Discount.id: "ID",
        Discount.code: "Код",
        Discount.discount_percent: "Процент",
        Discount.is_active: "Активна",
    }


class FlightCityAdmin(ModelView, model=FlightCity):
    """Административный интерфейс для городов в рейсах."""

    name = "Город в рейсе"
    name_plural = "Города в рейсах"
    icon = "fa-solid fa-plane-arrival"
    column_list = [
        FlightCity.id,
        FlightCity.flight_id,
        FlightCity.city_id,
        FlightCity.order,
    ]
    column_labels = {
        FlightCity.id: "ID",
        FlightCity.flight_id: "Рейс",
        FlightCity.city_id: "Город",
        FlightCity.order: "Порядок",
    }


class UserAdmin(ModelView, model=User):
    """Административный интерфейс для пользователей."""

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_list = [
        User.id,
        User.email,
        User.is_active,
        User.is_superuser,
        User.is_verified,
    ]
    column_labels = {
        User.id: "ID",
        User.email: "Email",
        User.is_active: "Активен",
        User.is_superuser: "Администратор",
        User.is_verified: "Подтвержден",
    }
