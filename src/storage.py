import json
from pathlib import Path
from typing import Dict, List
from .models import Flight, Booking, Passenger
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FLIGHTS_FILE = DATA_DIR / "flights.json"
BOOKINGS_FILE = DATA_DIR / "bookings.json"

ISO_FMT = "%Y-%m-%d %H:%M"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def load_flights() -> List[Flight]:
    _ensure_data_dir()
    if not FLIGHTS_FILE.exists():
        return []
    with FLIGHTS_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    flights: List[Flight] = []
    for item in raw:
        flights.append(
            Flight(
                number=item["number"],
                origin=item["origin"],
                destination=item["destination"],
                departure=datetime.strptime(item["departure"], ISO_FMT),
                arrival=datetime.strptime(item["arrival"], ISO_FMT),
                capacity=item["capacity"],
                booked_seats=item.get("booked_seats", 0),
            )
        )
    return flights


def save_flights(flights: List[Flight]) -> None:
    _ensure_data_dir()
    serializable = []
    for f in flights:
        serializable.append(
            {
                "number": f.number,
                "origin": f.origin,
                "destination": f.destination,
                "departure": f.departure.strftime(ISO_FMT),
                "arrival": f.arrival.strftime(ISO_FMT),
                "capacity": f.capacity,
                "booked_seats": f.booked_seats,
            }
        )
    with FLIGHTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


def load_bookings() -> List[Booking]:
    _ensure_data_dir()
    if not BOOKINGS_FILE.exists():
        return []
    with BOOKINGS_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    bookings: List[Booking] = []
    for item in raw:
        passenger = Passenger(
            name=item["passenger"]["name"],
            email=item["passenger"]["email"],
            phone=item["passenger"]["phone"],
        )
        bookings.append(
            Booking(
                booking_id=item["booking_id"],
                flight_number=item["flight_number"],
                passenger=passenger,
                seats=item["seats"],
                status=item.get("status", "CONFIRMED"),
            )
        )
    return bookings


def save_bookings(bookings: List[Booking]) -> None:
    _ensure_data_dir()
    serializable = []
    for b in bookings:
        serializable.append(
            {
                "booking_id": b.booking_id,
                "flight_number": b.flight_number,
                "passenger": {
                    "name": b.passenger.name,
                    "email": b.passenger.email,
                    "phone": b.passenger.phone,
                },
                "seats": b.seats,
                "status": b.status,
            }
        )
    with BOOKINGS_FILE.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)
