from .city import router as city_router
from .discount import router as discount_router
from .flight import router as flight_router
from .flightcity import router as flightcity_router
from .routecost import router as routecost_router
from .passenger import router as passenger_router
from .ticket import router as ticket_router


__all__ = [
    'city_router',
    'discount_router',
    'flight_router',
    'flightcity_router',
    'routecost_router',
    'passenger_router',
    'ticket_router',
]