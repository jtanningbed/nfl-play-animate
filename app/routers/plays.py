from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.play_response import PlayResponse, PlaySummaryResponse
from app.services import crud
from app.dependencies import get_db

router = APIRouter()


@router.get("/plays/{game_id}", response_model=PlaySummaryResponse)
def read_plays_by_game(
    game_id: int, db: Session = Depends(get_db)
) -> PlaySummaryResponse:
    try:
        return {"plays": crud.get_plays_by_game(db, game_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/play/{game_id}/{play_id}", response_model=PlayResponse)
def read_play_data(
    game_id: int, play_id: int, db: Session = Depends(get_db)
) -> PlayResponse:
    try:
        return crud.get_play_data(db, game_id, play_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
