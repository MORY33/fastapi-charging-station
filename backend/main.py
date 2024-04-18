from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from starlette.responses import RedirectResponse
from src.config.config import APP_NAME, VERSION
from src.routes.users import router as user_router
from src.routes.stations import router as charging_stations_router
from src.util.dependencies import get_db
from src.config.logger import setup_logger
from sqlalchemy.orm import Session
from sqlalchemy import text


app = FastAPI(
    title=APP_NAME,
    version=VERSION
)

setup_logger()

app.include_router(user_router)
app.include_router(charging_stations_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.get("/")
def docs():
    """
    Redirect to documentation.
    """
    return RedirectResponse(url="/docs/")

@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
