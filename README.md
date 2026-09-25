# Flight Management System (CLI)

Simple, modular Python CLI demonstrating flight scheduling and booking with basic persistence.

## Features
- Add flights with validation (schedule, capacity, unique number)
- List and search flights by origin, destination, and date
- Book seats with passenger info and availability checks
- Cancel bookings and free seats
- JSON file storage under `data/`

## Requirements
- Python 3.9+
- No external dependencies

## Run
```bash
python -m src.cli
```

## Data format
- Flights stored at `data/flights.json` with departure/arrival format `YYYY-MM-DD HH:MM`
- Bookings stored at `data/bookings.json`
