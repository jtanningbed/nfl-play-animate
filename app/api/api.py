from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.services import crud

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/weeks")
def read_weeks(db: Session = Depends(get_db)):
    return {"weeks": crud.get_weeks(db)}


@router.get("/games/{week}")
def read_games_by_week(week: int, db: Session = Depends(get_db)):
    return {"games": crud.get_games_by_week(db, week)}


@router.get("/plays/{game_id}")
def read_plays_by_game(game_id: int, db: Session = Depends(get_db)):
    return {"plays": crud.get_plays_by_game(db, game_id)}


@router.get("/play/{game_id}/{play_id}")
def read_play_data(game_id: int, play_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_play_data(db, game_id, play_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
