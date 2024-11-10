from fastapi import FastAPI
from app.routers import games, plays, weeks

app = FastAPI()

# Include the API router
app.include_router(games.router, prefix="/api")
app.include_router(plays.router, prefix="/api")
app.include_router(weeks.router, prefix="/api")
