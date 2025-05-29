import csv
from datetime import datetime
from pathlib import Path
from typing import Type

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import City, Flight, RouteCost


async def load_cities(session: AsyncSession, file_path: Path) -> None:
    """Загрузка городов из CSV файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = City(name=row["name"], code=row["code"])
            session.add(city)
    await session.commit()


async def load_flights(session: AsyncSession, file_path: Path) -> None:
    """Загрузка рейсов из CSV файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            flight = Flight(
                number=row["number"],
                date_flight=datetime.strptime(row["date_flight"], "%Y-%m-%d").date(),
                board=row["board"],
                status=row["status"],
            )
            session.add(flight)
    await session.commit()


async def load_route_costs(session: AsyncSession, file_path: Path) -> None:
    """Загрузка стоимости маршрутов из CSV файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            route_cost = RouteCost(
                from_city_id=int(row["from_city_id"]),
                to_city_id=int(row["to_city_id"]),
                cost=float(row["cost"]),
            )
            session.add(route_cost)
    await session.commit()


async def load_data_from_csv(
    session: AsyncSession, model: Type[Table], file_path: Path
) -> None:
    """Общая функция для загрузки данных из CSV."""
    loaders = {
        City: load_cities,
        Flight: load_flights,
        RouteCost: load_route_costs,
    }

    if model not in loaders:
        raise ValueError(f"Загрузчик для модели {model.__name__} не найден")

    await loaders[model](session, file_path)
