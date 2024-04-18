from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type, Generic, TypeVar, Any, List, Optional

T = TypeVar('T')  # ORM Model type
D = TypeVar('D')  # Pydantic schema

class CRUD(Generic[T, D]):
    def __init__(self, model: Type[T], db_session: Session):
        self.model = model
        self.db = db_session

    def create(self, obj_in: D) -> T:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, id: Any) -> T:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int, limit: int, name: Optional[str] = None) -> List[T]:
        query = self.db.query(self.model)
        if name:
            query = query.filter(self.model.name == name)
        return query.offset(skip).limit(limit).all()

    def update(self, db_obj: T, obj_in: D) -> T:
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
