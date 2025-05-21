from .city import (
    CityCreate,
    CityDB,
    CityUpdate,
)
from .flight import (
    FlightCreate,
    FlightDB,
    FlightUpdate,
)
from .discount import (
    DiscountCreate,
    DiscountDB,
    DiscountUpdate,
)
from .flightcity import (
    CityFlights,
    FlightCities,
    FlightCityCreate,
    FlightCityDB,
    FlightCityResponse,
    FlightCityUpdate,
)
from .passenger import (
    PassengerCreate,
    PassengerDB,
    PassengerTickets,
    PassengerUpdate,
)
from .routecost import (
    RoutCostDB,
    RouteCostCreate,
    RouteCostResponse,
    RouteCostUpdate,
)
from .ticket import (
    TicketCreate,
    TicketDB,
    TicketResponse,
    TicketStatus,
    TicketUpdate,
)
from .user import (
    UserCreate,
    UserRead,
    UserUpdate,
)
