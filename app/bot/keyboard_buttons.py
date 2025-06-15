from telegram import (
    InlineKeyboardButton,
)

inline_about_project = InlineKeyboardButton(
    text='О приложении',
    callback_data='about_project',
)
inline_about_project_not_reg = InlineKeyboardButton(
    text='О приложении',
    callback_data='about_project_not_reg',
)

inline_back_to_main_menu = InlineKeyboardButton(
    text='В главное меню',
    callback_data='to_main_menu',
)
inline_booking = InlineKeyboardButton(
    text='Запись',
    callback_data='to_booking'
)
inline_flights = InlineKeyboardButton(
    text='Рейсы',
    callback_data='to_flights'
)
inline_cities = InlineKeyboardButton(
    text='Нас. пункты',
    callback_data='to_cities'
)

inline_exit_app = InlineKeyboardButton(
    text='Завершить работу',
    callback_data='exit_app',
)

inline_no_action = InlineKeyboardButton(
    text=' ',
    callback_data='no_action',
)


def get_inl_cities_buttons(cities: list[dict]) -> list:
    """Создаёт inline-кнопки для городов."""
    cities_buttons = []
    for city in cities:
        cities_buttons.append(
            InlineKeyboardButton(
                text=f'{city["name"]} {city["code"]}',
                callback_data=f"about_city_id_{city['city_id']}",
            ),
        )
    return cities_buttons


def get_inl_flights_buttons(flights: list[dict]) -> list:
    """Создаёт inline-кнопки для городов."""
    flights_buttons = []
    for flight in flights:
        flights_buttons.append(
            InlineKeyboardButton(
                text=f'{flight["number"]} {flight["date"]}',
                callback_data=f"about_flight_id_{flight['flight_id']}",
            ),
        )
    return flights_buttons
