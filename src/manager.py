import uuid
from datetime import datetime
from typing import List, Optional
from .models import Flight, Booking, Passenger
from . import storage


def parse_datetime(text: str) -> datetime:
    return datetime.strptime(text, storage.ISO_FMT)


def list_flights() -> List[Flight]:
    return storage.load_flights()


def find_flight(number: str) -> Optional[Flight]:
    flights = storage.load_flights()
    return next((f for f in flights if f.number == number), None)


def add_flight(number: str, origin: str, destination: str, departure: str, arrival: str, capacity: int) -> Flight:
    flights = storage.load_flights()
    if any(f.number == number for f in flights):
        raise ValueError("Flight number already exists")
    flight = Flight(
        number=number,
        origin=origin,
        destination=destination,
        departure=parse_datetime(departure),
        arrival=parse_datetime(arrival),
        capacity=capacity,
    )
    flight.validate()
    flights.append(flight)
    storage.save_flights(flights)
    return flight


def remove_flight(number: str) -> None:
    flights = storage.load_flights()
    updated = [f for f in flights if f.number != number]
    if len(updated) == len(flights):
        raise ValueError("Flight not found")
    storage.save_flights(updated)


def list_bookings() -> List[Booking]:
    return storage.load_bookings()


def add_booking(flight_number: str, passenger_name: str, passenger_email: str, passenger_phone: str, seats: int) -> Booking:
    flights = storage.load_flights()
    flight = next((f for f in flights if f.number == flight_number), None)
    if not flight:
        raise ValueError("Flight not found")
    if flight.available_seats() < seats:
        raise ValueError("Not enough seats available")

    passenger = Passenger(passenger_name, passenger_email, passenger_phone)
    passenger.validate()
    booking = Booking(
        booking_id=str(uuid.uuid4())[:8],
        flight_number=flight.number,
        passenger=passenger,
        seats=seats,
    )
    booking.validate()

    bookings = storage.load_bookings()
    bookings.append(booking)
    storage.save_bookings(bookings)

    flight.booked_seats += seats
    flight.validate()
    storage.save_flights(flights)
    return booking


def cancel_booking(booking_id: str) -> None:
    bookings = storage.load_bookings()
    booking = next((b for b in bookings if b.booking_id == booking_id), None)
    if not booking:
        raise ValueError("Booking not found")
    if booking.status == "CANCELLED":
        return
    flights = storage.load_flights()
    flight = next((f for f in flights if f.number == booking.flight_number), None)
    if flight:
        flight.booked_seats = max(flight.booked_seats - booking.seats, 0)
        flight.validate()
        storage.save_flights(flights)
    booking.status = "CANCELLED"
    storage.save_bookings(bookings)


def search_flights(origin: Optional[str] = None, destination: Optional[str] = None, date: Optional[str] = None) -> List[Flight]:
    flights = storage.load_flights()
    results = flights
    if origin:
        results = [f for f in results if f.origin.lower() == origin.lower()]
    if destination:
        results = [f for f in results if f.destination.lower() == destination.lower()]
    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        results = [f for f in results if f.departure.date() == date_obj]
    return results
