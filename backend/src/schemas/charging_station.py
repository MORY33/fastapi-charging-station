from pydantic import BaseModel, Field, IPvAnyAddress
from uuid import UUID

class ChargingStationTypeCreate(BaseModel):
    name: str = Field(..., example="Fast Charging Station")
    plug_count: int = Field(..., ge=1, example=4)
    efficiency: float = Field(..., gt=0, example=0.9)
    current_type: str = Field(..., example="AC")

class ChargingStationType(BaseModel):
    id: UUID
    name: str
    plug_count: int
    efficiency: float
    current_type: str

    class Config:
        from_attributes = True

class ChargingStationCreate(BaseModel):
    name: str = Field(..., example="Station 1")
    device_id: UUID
    ip_address: IPvAnyAddress = Field(..., example="192.168.1.1")
    firmware_version: str = Field(..., example="v1.2.3")
    type_id: UUID

class ChargingStation(BaseModel):
    id: UUID
    name: str
    device_id: UUID
    ip_address: IPvAnyAddress
    firmware_version: str
    type_id: UUID

    class Config:
        from_attributes = True

class ConnectorCreate(BaseModel):
    name: str = Field(..., example="Connector A")
    priority: bool = Field(default=False, example=True)

class Connector(BaseModel):
    id: UUID
    name: str
    priority: bool
    charging_station_id: UUID

    class Config:
        from_attributes = True
