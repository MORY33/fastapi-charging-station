from pydantic import BaseModel, Field, IPvAnyAddress, UUID4
from typing import List, Optional
from uuid import UUID
from src.config.database import Base
from src.models.charging_station import StationTypeEnum, CurrentType

# Charging station type
class ChargingStationTypeSchema(BaseModel):
    id: UUID
    name: StationTypeEnum
    plug_count: int
    efficiency: float
    current_type: CurrentType

    # class Config:
    #     from_attributes = True


class ChargingStationTypeCreateSchema(BaseModel):

    name: StationTypeEnum = Field(..., example="TYPE_A")
    plug_count: int = Field(..., ge=1, example=4)
    efficiency: float = Field(..., gt=0, example=0.9)
    current_type: CurrentType = Field(..., example="AC")

    # class Config:
    #     from_attributes = True

#connector
class ConnectorCreateSchema(BaseModel):
    name: str = Field(..., example="Connector A")
    priority: bool = Field(default=False, example=True)
    charging_station_id: UUID

    # class Config:
    #     from_attributes = True

class ConnectorSchema(BaseModel):
    id: UUID
    name: str
    priority: bool
    charging_station_id: UUID

    # class Config:
    #     from_attributes = True


# charging station

class ChargingStationCreateSchema(BaseModel):
    name: str = Field(..., example="Station 1")
    device_id: UUID
    ip_address: str = Field(..., example="192.168.1.1")
    firmware_version: str = Field(..., example="v1.2.3")
    type_id: UUID

    # class Config:
    #     from_attributes = True

class ChargingStationSchema(BaseModel):
    id: UUID
    name: str
    device_id: UUID
    ip_address: str
    firmware_version: str
    type_id: UUID
    connectors: List[ConnectorSchema]

    # class Config:
    #     from_attributes = True



