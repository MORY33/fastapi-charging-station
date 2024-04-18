from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
import uuid
import enum
from src.config.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class CurrentType(enum.Enum):
    AC = "AC"
    DC = "DC"


class StationTypeEnum(enum.Enum):
    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"
    TYPE_C = "TYPE_C"
    TYPE_D = "TYPE_D"
    TYPE_E = "TYPE_E"

class ChargingStation(Base):
    __tablename__ = 'charging_stations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    device_id = Column(UUID(as_uuid=True), unique=True, default=generate_uuid)
    ip_address = Column(String, unique=True)
    firmware_version = Column(String)
    type_id = Column(UUID(as_uuid=True), ForeignKey('charging_station_types.id'))
    type = relationship('ChargingStationType', back_populates='charging_stations')

    connectors = relationship('Connector', back_populates='charging_station')

    __unique_fields__ = ['name']
    @validates('connectors')
    def validate_connectors(self, key, connector):
        if len(self.connectors) >= self.type.plug_count:
            raise ValueError("Cannot add more connectors than the plug_count of the charging station's type.")

        if connector.priority and any(c.priority for c in self.connectors if c is not connector):
            raise ValueError("There can only be one priority connector per charging station.")

        return connector

class ChargingStationType(Base):
    __tablename__ = 'charging_station_types'

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    name = Column(Enum(StationTypeEnum), index=True, unique=True)
    plug_count = Column(Integer)
    efficiency = Column(Float)
    current_type = Column(Enum(CurrentType))

    charging_stations = relationship('ChargingStation', back_populates='type')

    __unique_fields__ = ['name']
class Connector(Base):
    __tablename__ = 'connectors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    priority = Column(Boolean, default=False)
    charging_station_id = Column(UUID(as_uuid=True), ForeignKey('charging_stations.id'))

    charging_station = relationship('ChargingStation', back_populates='connectors')
