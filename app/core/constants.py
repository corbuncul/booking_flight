from enum import StrEnum

BOARD_MAX_LENGHT = 10
CODE_MAX_LENGHT = 5
CODE_MIN_LENGHT = 3
DOC_MAX_LENGHT = 15
FLIGHT_MAX_LENGHT = 10
FLIGHT_MIN_LENGHT = 5
NAME_MAX_LENGHT = 100
PHONE_MAX_LENGHT = 15
TICKET_MAX_LENGHT = 15


class FlightStatus(StrEnum):
    PLANNED = 'planned'
    DEPARTED = 'departed'
    CANCELLED = 'cancelled'


class TicketStatus(StrEnum):
    BOOKED = 'booked'
    PAID = 'paid'
    CANCELLED = 'cancelled'
