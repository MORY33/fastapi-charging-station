from sqlalchemy import Column, Integer, String
from src.config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    def __repr__(self):
        return f"id: {self.id}, name: {self.username}"