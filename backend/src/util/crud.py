from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type, Generic, TypeVar, Any, List, Optional
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from src.models.charging_station import StationTypeEnum


T = TypeVar('T')  # ORM Model type
D = TypeVar('D')  # Pydantic schema

class CRUD(Generic[T, D]):
    def __init__(self, model: Type[T], db_session: Session):
        self.model = model
        self.db = db_session

    def create(self, obj_in: D) -> T:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        try:
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        return db_obj

    def get(self, id: Any) -> T:
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_all(self, skip: int, limit: int, name: Optional[str] = None) -> List[T]:
        query = self.db.query(self.model)
        if name:
            query = query.filter(self.model.name == name)
        return query.offset(skip).limit(limit).all()


    def update(self, id: Any, obj_in: D) -> T:
        db_obj = self.db.query(self.model).get(id)
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Object not found")
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: Any):
        obj = self.db.query(self.model).get(id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Object not found")
        self.db.delete(obj)
        self.db.commit()
        return {"ok": True}

    def get_all_by_type(self, station_type: StationTypeEnum, skip: int, limit: int) -> List[T]:
        return (
            self.db.query(self.model)
            .filter(self.model.name == station_type)
            .offset(skip)
            .limit(limit)
            .all()
        )