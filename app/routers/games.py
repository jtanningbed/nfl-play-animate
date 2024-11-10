from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.game import GameResponse
from app.services import crud
from app.dependencies import get_db

router = APIRouter()


@router.get("/games/{week}", response_model=GameResponse)
def read_games_by_week(week: int, db: Session = Depends(get_db)):
    try:
        return {"games": crud.get_games_by_week(db, week)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
