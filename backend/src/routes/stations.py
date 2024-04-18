from fastapi import FastAPI, HTTPException, Depends, Path, Query, APIRouter
from typing import List, Optional
from src.models.charging_station import ChargingStation, ChargingStationType, Connector, CurrentType
from src.models.user import User as UserModel
from src.schemas.charging_station import ChargingStationCreate, ChargingStationTypeCreate, ConnectorCreate
from sqlalchemy.orm import Session
from src.util.dependencies import get_db
from src.schemas.pagination import PaginationParams
from src.auth.auth import get_current_user
from src.util.crud import CRUD

router = APIRouter()
@router.post("/charging_station_types/", response_model=ChargingStationTypeCreate)
def create_charging_station_type(
    charging_station_type: ChargingStationTypeCreate,
    db: Session = Depends(get_db),
    # current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.create(charging_station_type)

@router.get("/charging_station_types/", response_model=List[ChargingStationTypeCreate])
def list_charging_station_types(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.get_all(pagination.skip, pagination.limit)


@router.get("/charging_station_types/{type_id}", response_model=ChargingStationTypeCreate)
def get_charging_station_type(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.get(type_id)

@router.post("/charging_stations/", response_model=ChargingStationCreate)
def create_charging_station(
    charging_station: ChargingStationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    return crud.create(charging_station)

@router.get("/charging_stations/", response_model=List[ChargingStationCreate])
def list_charging_stations(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    return crud.get_all(pagination.skip, pagination.limit)

@router.get("/charging_stations/{station_id}", response_model=ChargingStationCreate)
def get_charging_station(
    station_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStation, db)
    return crud.get(station_id)

@router.post("/charging_stations/{station_id}/connectors/", response_model=ConnectorCreate)
def add_connector_to_station(
    station_id: str,
    connector: ConnectorCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(Connector, db)
    return crud.create(connector)

@router.get("/charging_stations/{station_id}/connectors/", response_model=List[ConnectorCreate])
def list_connectors_for_station(
    station_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(Connector, db)
    return crud.get_all_for_station(station_id)

@router.put("/charging_station_types/{type_id}", response_model=ChargingStationTypeCreate)
def update_charging_station_type(
    type_id: str,
    charging_station_type: ChargingStationTypeCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.update(type_id, charging_station_type)

@router.delete("/charging_station_types/{type_id}", status_code=204)
def delete_charging_station_type(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    crud = CRUD(ChargingStationType, db)
    return crud.delete(type_id)
