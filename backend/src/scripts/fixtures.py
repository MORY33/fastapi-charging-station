from src.config.database import SessionLocal
from src.models.charging_station import ChargingStationType, ChargingStation, Connector, StationTypeEnum
import uuid


def generate_uuid():
    return str(uuid.uuid4())


def load_fixtures(db):

    station_types = [
        ChargingStationType(id=generate_uuid(), name=StationTypeEnum.TYPE_A.value, plug_count=2, efficiency=0.85,
                            current_type="AC"),
        ChargingStationType(id=generate_uuid(), name=StationTypeEnum.TYPE_B.value, plug_count=4, efficiency=0.90,
                            current_type="DC"),
        ChargingStationType(id=generate_uuid(), name=StationTypeEnum.TYPE_C.value, plug_count=1, efficiency=0.80,
                            current_type="AC"),
        ChargingStationType(id=generate_uuid(), name=StationTypeEnum.TYPE_D.value, plug_count=3, efficiency=0.75,
                            current_type="DC"),
        ChargingStationType(id=generate_uuid(), name=StationTypeEnum.TYPE_E.value, plug_count=2, efficiency=0.95,
                            current_type="AC"),
    ]

    db.add_all(station_types)
    db.commit()

    # Create charging station for each type
    for index, station_type in enumerate(station_types, start=1):
        station = ChargingStation(
            id=generate_uuid(),
            name=f"Station {index}",
            device_id=generate_uuid(),
            ip_address=f"192.168.1.{index}",
            firmware_version=f"v{index}.0.0",
            type_id=station_type.id,
        )
        db.add(station)
        db.commit()

        # Create specified number of connectors for the station
        priority_set = False
        for plug_index in range(station_type.plug_count):
            priority = True if plug_index == 0 and not priority_set else False
            if priority:
                priority_set = True

            connector = Connector(
                id=generate_uuid(),
                name=f"Connector {plug_index} for Station {index}",
                priority=priority,
                charging_station_id=station.id,
            )
            db.add(connector)
        db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    load_fixtures(db)
