from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.week import WeekResponse
from app.services import crud
from app.dependencies import get_db

router = APIRouter()


@router.get("/weeks", response_model=WeekResponse)
def read_weeks(db: Session = Depends(get_db)) -> WeekResponse:
    try:
        return {"weeks": crud.get_weeks(db)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
