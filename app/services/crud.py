import pandas as pd
from sqlalchemy.orm import Session
import numpy as np


def get_weeks(db: Session) -> list:
    # Use the connection from the session
    with db.connection() as connection:
        return pd.read_sql("SELECT DISTINCT week FROM games ORDER BY week", connection)[
            "week"
        ].tolist()


def get_games_by_week(db: Session, week: int) -> list[dict]:
    with db.connection() as connection:
        return pd.read_sql(
            "SELECT gameId, homeTeamAbbr, visitorTeamAbbr FROM games WHERE week = %s ORDER BY gameId",
            connection,
            params=(week,),
        ).to_dict(orient="records")


def get_plays_by_game(db: Session, game_id: int) -> list[dict]:
    with db.connection() as connection:
        return pd.read_sql(
            "SELECT playId, playDescription, quarter, gameClock FROM plays WHERE gameId = %s ORDER BY quarter, gameClock DESC",
            connection,
            params=(game_id,),
        ).to_dict(orient="records")


def get_play_data(db: Session, game_id: int, play_id: int) -> dict:
    gameattrs = "gameid,hometeamabbr,visitorteamabbr"
    playattrs = (
        "gameid,playid,playdescription,down,quarter,absoluteyardlinenumber,yardstogo"
    )
    trackingattrs = (
        "gameid,playid,nflid,playdirection,club,frameid,s,a,dir,dis,displayname,x,y"
    )

    with db.connection() as connection:
        game_data = pd.read_sql(
            f"SELECT {gameattrs} FROM games WHERE gameId = %s",
            connection,
            params=(game_id,),
        )
        play_data = pd.read_sql(
            f"SELECT {playattrs} FROM plays WHERE gameId = %s AND playId = %s",
            connection,
            params=(game_id, play_id),
        )
        tracking_data = pd.read_sql(
            f"SELECT {trackingattrs} FROM tracking_data WHERE gameId = %s AND playId = %s",
            connection,
            params=(game_id, play_id),
        )

    # Handle NaN and infinity values for 'dir' column
    tracking_data["dir"] = (
        tracking_data["dir"].replace([np.inf, -np.inf], np.nan).fillna(0)
    )

    # Handle null values for 'nflid' column
    tracking_data["nflid"] = tracking_data["nflid"].fillna(0).astype(int)

    return {
        "game_data": game_data.to_dict(orient="records"),
        "play_data": play_data.to_dict(orient="records"),
        "tracking_data": tracking_data.to_dict(orient="records"),
    }
