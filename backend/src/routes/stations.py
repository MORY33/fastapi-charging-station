from fastapi import FastAPI, HTTPException, Depends, Path, Query, APIRouter, Query
from typing import List, Optional
from src.models.charging_station import ChargingStation, ChargingStationType, Connector, CurrentType
from src.models.user import User as UserModel
from src.schemas.charging_station import ChargingStationTypeSchema, \
    ChargingStationTypeCreateSchema, \
    ChargingStationSchema,  \
    ChargingStationCreateSchema, \
    ConnectorSchema, \
    ConnectorCreateSchema
from sqlalchemy.orm import Session
from src.util.dependencies import get_db
from src.schemas.pagination import PaginationParams
from src.auth.auth import get_current_user
from src.util.crud import CRUD
from uuid import UUID
from src.models.charging_station import StationTypeEnum

router = APIRouter()

#-------------------------------CHARGING STATION TYPES---------------------------------------------------------
@router.post("/charging_station_types/", response_model=ChargingStationTypeSchema)
def create_charging_station_type(
    charging_station_type: ChargingStationTypeCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.create(charging_station_type)


@router.get("/charging_station_types/", response_model=List[ChargingStationTypeSchema])
def list_charging_station_types(
    pagination: PaginationParams = Depends(),
    station_type: Optional[StationTypeEnum] = Query(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    if station_type:
        return crud.get_all_by_type(station_type, pagination.skip, pagination.limit)
    else:
        return crud.get_all(pagination.skip, pagination.limit)

@router.get("/charging_station_types/{type_id}", response_model=ChargingStationTypeSchema)
def get_charging_station_type(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.get(type_id)

@router.patch("/charging_station_types/{type_id}", response_model=ChargingStationTypeSchema)
def update_charging_station_type(
    type_id: UUID,
    charging_station_type: ChargingStationTypeCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    updated_type = crud.update(type_id, charging_station_type)
    if updated_type is None:
        raise HTTPException(status_code=404, detail="Charging station type not found")

    return updated_type

@router.delete("/charging_stations_types/{type_id}", status_code=204)
def delete_charging_station_type(type_id: UUID, db: Session = Depends(get_db),
                            current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.delete(type_id)

#-------------------------------CHARGING STATIONS -------------------------------------------------------------

@router.post("/charging_stations/", response_model=ChargingStationSchema)
def create_charging_station(
    charging_station: ChargingStationCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    return crud.create(charging_station)


@router.get("/charging_stations/", response_model=List[ChargingStationSchema])
def list_charging_stations(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    return crud.get_all(pagination.skip, pagination.limit)

@router.get("/charging_station/{charging_station_id}", response_model=ChargingStationSchema)
def get_charging_station(
    charging_station_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    return crud.get(charging_station_id)


@router.patch("/charging_station/{charging_station_id}", response_model=ChargingStationSchema)
def update_charging_station(
    charging_station_id: UUID,
    charging_station: ChargingStationCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    updated_station = crud.update(charging_station_id, charging_station)
    if updated_station is None:
        raise HTTPException(status_code=404, detail="Charging station not found")
    return updated_station

@router.delete("/charging_station/{charging_station_id}", status_code=204)
def delete_charging_station(charging_station_id: UUID, db: Session = Depends(get_db),
                            current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    return crud.delete(charging_station_id)


#------------------------------- CONNECTORS --------------------------------------------------------------------

@router.post("/connectors/", response_model=ConnectorSchema)
def create_connector(
    connector: ConnectorCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(Connector, db)
    return crud.create(connector)

@router.get("/connectors/", response_model=List[ConnectorSchema])
def list_charging_stations(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(Connector, db)
    return crud.get_all(pagination.skip, pagination.limit)

@router.get("/connectors/{connector_id}", response_model=ConnectorSchema)
def get_connector(
    connector_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(Connector, db)
    return crud.get(connector_id)


@router.patch("/connectors/{connector_id}", response_model=ConnectorSchema)
def update_connector(
    connector_id: str,
    connector: ConnectorCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(Connector, db)
    updated_connector = crud.update(connector_id, connector)
    if updated_connector is None:
        raise HTTPException(status_code=404, detail="Connector not found")
    return updated_connector

@router.delete("/connectors/{connector_id}", status_code=204)
def delete_connector(connector_id: str, db: Session = Depends(get_db),
                            current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(Connector, db)
    return crud.delete(connector_id)

