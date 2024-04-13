from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

db_username = os.getenv("DB_USER", "user")
db_password = os.getenv("DB_PASS", "password123")
db_host = os.getenv("DB_HOST", "db")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "example")

connection_string = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# engine = create_engine(connection_string, echo=False)
engine = create_engine(connection_string, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


