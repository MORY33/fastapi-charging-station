# FastAPI Charging Station API

This is a FastAPI-based API for managing charging stations and connectors. It provides endpoints for creating, listing, updating, and deleting charging station types, charging stations, and connectors.

## Endpoints

### Charging Station Types

- `POST /charging_station_types/`: Create a new charging station type.
- `GET /charging_station_types/`: Get a list of all charging station types.
- `GET /charging_station_types/{type_id}`: Get details of a specific charging station type.
- `PATCH /charging_station_types/{type_id}`: Update a charging station type.
- `DELETE /charging_station_types/{type_id}`: Delete a charging station type.

### Charging Stations

- `POST /charging_stations/`: Create a new charging station.
- `GET /charging_stations/`: Get a list of all charging stations.
- `GET /charging_station/{charging_station_id}`: Get details of a specific charging station.
- `PATCH /charging_station/{charging_station_id}`: Update a charging station.
- `DELETE /charging_station/{charging_station_id}`: Delete a charging station.

### Connectors

- `POST /connectors/`: Create a new connector.
- `GET /connectors/`: Get a list of all connectors.
- `GET /connectors/{connector_id}`: Get details of a specific connector.
- `PATCH /connectors/{connector_id}`: Update a connector.
- `DELETE /connectors/{connector_id}`: Delete a connector.

## Running the Application with Docker Compose

To run the application using Docker Compose, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. .env is intentionally in git, you do not have to update it.
4. Run the following command to start the application:

```bash
docker-compose up --build
```

Running Tests and Loading Fixtures
----------------------------------

Run the following command to start the tests:

```bash
docker-compose run web poetry run pytest
```

Run the following command to load fixtures:
```bash
docker-compose exec web poetry run python -m src.scripts.fixtures

```


## Dependencies
- Python 3.12 or higher
- Docker version 25.0.3 or higher
- Docker Compose version v2.2.3 or higher
