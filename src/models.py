from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Passenger:
    name: str
    email: str
    phone: str

    def validate(self) -> None:
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError("Passenger name must be at least 2 characters")
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email address")
        digits = [c for c in self.phone if c.isdigit()]
        if len(digits) < 10:
            raise ValueError("Phone number must have at least 10 digits")


@dataclass
class Flight:
    number: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    capacity: int
    booked_seats: int = 0

    def available_seats(self) -> int:
        return max(self.capacity - self.booked_seats, 0)

    def validate(self) -> None:
        if self.origin == self.destination:
            raise ValueError("Origin and destination must differ")
        if self.departure >= self.arrival:
            raise ValueError("Departure time must be before arrival time")
        if self.capacity <= 0:
            raise ValueError("Capacity must be positive")
        if self.booked_seats < 0 or self.booked_seats > self.capacity:
            raise ValueError("Booked seats must be within capacity")


@dataclass
class Booking:
    booking_id: str
    flight_number: str
    passenger: Passenger
    seats: int
    status: str = field(default="CONFIRMED")  # CONFIRMED or CANCELLED

    def validate(self) -> None:
        if self.seats <= 0:
            raise ValueError("Seats booked must be positive")
        self.passenger.validate()
        if self.status not in {"CONFIRMED", "CANCELLED"}:
            raise ValueError("Invalid booking status")
