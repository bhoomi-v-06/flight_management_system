import sys
from typing import Callable, Dict
from . import manager
from .models import Flight, Booking


def print_flights(flights):
    if not flights:
        print("No flights found")
        return
    for f in flights:
        print(
            f"{f.number}: {f.origin} -> {f.destination} | {f.departure.strftime('%Y-%m-%d %H:%M')} - {f.arrival.strftime('%Y-%m-%d %H:%M')} | Capacity: {f.capacity} | Booked: {f.booked_seats} | Available: {f.available_seats()}"
        )


def print_bookings(bookings):
    if not bookings:
        print("No bookings found")
        return
    for b in bookings:
        print(
            f"{b.booking_id}: Flight {b.flight_number} | Passenger: {b.passenger.name} | Seats: {b.seats} | Status: {b.status}"
        )


def handle_add_flight():
    number = input("Flight number: ")
    origin = input("Origin: ")
    destination = input("Destination: ")
    departure = input("Departure (YYYY-MM-DD HH:MM): ")
    arrival = input("Arrival (YYYY-MM-DD HH:MM): ")
    capacity = int(input("Capacity: "))
    flight = manager.add_flight(number, origin, destination, departure, arrival, capacity)
    print(f"Added flight {flight.number}")


def handle_list_flights():
    print_flights(manager.list_flights())


def handle_search_flights():
    origin = input("Origin (blank to skip): ") or None
    destination = input("Destination (blank to skip): ") or None
    date = input("Date YYYY-MM-DD (blank to skip): ") or None
    results = manager.search_flights(origin, destination, date)
    print_flights(results)


def handle_add_booking():
    flight_number = input("Flight number: ")
    name = input("Passenger name: ")
    email = input("Passenger email: ")
    phone = input("Passenger phone: ")
    seats = int(input("Seats to book: "))
    booking = manager.add_booking(flight_number, name, email, phone, seats)
    print(f"Booking confirmed with ID {booking.booking_id}")


def handle_list_bookings():
    print_bookings(manager.list_bookings())


def handle_cancel_booking():
    booking_id = input("Booking ID to cancel: ")
    manager.cancel_booking(booking_id)
    print("Booking cancelled")


actions: Dict[str, Callable[[], None]] = {
    "1": handle_add_flight,
    "2": handle_list_flights,
    "3": handle_search_flights,
    "4": handle_add_booking,
    "5": handle_list_bookings,
    "6": handle_cancel_booking,
}


def main():
    menu = """\nFlight Management System\n1. Add Flight\n2. List Flights\n3. Search Flights\n4. Add Booking\n5. List Bookings\n6. Cancel Booking\n0. Exit\nSelect option: """
    while True:
        choice = input(menu).strip()
        if choice == "0":
            print("Goodbye")
            return
        action = actions.get(choice)
        if not action:
            print("Invalid option\n")
            continue
        try:
            action()
        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
