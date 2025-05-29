from datetime import date, datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import TicketStatus
from app.core.db import get_async_session
from app.crud import city_crud, flight_crud, passenger_crud, ticket_crud
from app.schemas import PassengerCreate, TicketCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def booking_page(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    """Страница бронирования билета."""
    cities = await city_crud.get_all(session)
    return templates.TemplateResponse(
        "booking.html", {"request": request, "cities": cities}
    )


@router.post("/", response_class=HTMLResponse)
async def create_booking(
    request: Request,
    from_city: int = Form(...),
    to_city: int = Form(...),
    flight_date: date = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    birth_date: date = Form(...),
    document_number: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    """Обработка формы бронирования."""
    # Проверка валидности городов
    if from_city == to_city:
        raise HTTPException(
            status_code=400,
            detail=("Города отправления и прибытия должны различаться")
        )

    # Создание пассажира
    passenger_data = PassengerCreate(
        name=first_name,
        surname=last_name,
        birthday=birth_date,
        doc_number=document_number,
    )
    passenger = await passenger_crud.create(passenger_data, session)

    # Получение подходящего рейса
    flight = await flight_crud.get_flight_by_date_cities(
        session, flight_date, from_city, to_city
    )
    if not flight:
        raise HTTPException(
            status_code=404, detail="Нет доступных рейсов на указанную дату"
        )

    # Создание билета
    ticket_data = TicketCreate(
        passenger_id=passenger.id,
        flight_id=flight.id,
        from_city_id=from_city,
        to_city_id=to_city,
        status=TicketStatus.BOOKED,
        created_at=datetime.now(),
    )
    ticket = await ticket_crud.create(ticket_data, session)

    # Получение списка городов для формы
    cities = await city_crud.get_all(session)

    return templates.TemplateResponse(
        "booking.html",
        {"request": request, "cities": cities, "ticket": ticket}
    )
