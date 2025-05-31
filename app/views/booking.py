from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import TicketStatus
from app.core.db import get_async_session
from app.core.logger import logger
from app.crud import (
    city_crud,
    flight_crud,
    passenger_crud,
    routecost_crud,
    ticket_crud
)
from app.services.discount import apply_discount
from app.schemas import PassengerCreate, TicketCreate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def booking_page(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    """Страница бронирования билета."""
    cities = await city_crud.get_all(session)
    logger.info('Пользователь бронирует.')
    return templates.TemplateResponse(
        'booking.html', {'request': request, 'cities': cities}
    )


@router.post('/', response_class=HTMLResponse)
async def create_booking(
    request: Request,
    from_city: int = Form(...),
    to_city: int = Form(...),
    date_flight: date = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
    birthday: date = Form(...),
    doc_number: str = Form(...),
    email: str = Form(...),
    tg_id: int = Form(...),
    phone: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    """Обработка формы бронирования."""
    # Проверка валидности городов
    if from_city == to_city:
        raise HTTPException(
            status_code=400,
            detail=('Города отправления и прибытия должны различаться')
        )

    # Создание пассажира
    passenger_data = PassengerCreate(
        name=name,
        surname=surname,
        birthday=birthday,
        doc_number=doc_number,
        email=email,
        tg_id=tg_id,
        phone=phone,
    )
    passenger = await passenger_crud.create(passenger_data, session)
    logger.info(f'Создан пассажир {passenger}')

    # Получение подходящего рейса
    flight = await flight_crud.get_flight_by_date_cities(
        session, date_flight, from_city, to_city
    )
    if not flight:
        logger.error(f'Нет доступных рейсов на указанную дату {date_flight}')
        raise HTTPException(
            status_code=404, detail='Нет доступных рейсов на указанную дату'
        )

    discount_code = ''
    today = date.today()
    age = relativedelta(today, passenger.birthday)
    if age.years < 2:
        # РМГ - Ребенок до 2 лет
        discount_code = 'РМГ'
    elif age.years < 12:
        discount_code = 'РБГ'
    original_price = await routecost_crud.get_cost_by_cities(
        session,
        from_city_id=from_city,
        to_city_id=to_city
    )
    final_price = await apply_discount(
        session, discount_code, original_price.cost
    )
    if discount_code != '':
        logger.info(f'Применена скидка {discount_code}')
    # Создание билета
    ticket_data = TicketCreate(
        passenger_id=passenger.id,
        flight_id=flight.id,
        from_city_id=from_city,
        to_city_id=to_city,
        discount_code=discount_code,
        final_price=final_price,
        status=TicketStatus.BOOKED,
        created_at=datetime.now(),
    )
    ticket = await ticket_crud.create(ticket_data, session)
    logger.info(f'Создана запись {ticket}')

    # Получение списка городов для формы
    cities = await city_crud.get_all(session)

    return templates.TemplateResponse(
        'booking.html',
        {'request': request, 'cities': cities, 'ticket': ticket}
    )
