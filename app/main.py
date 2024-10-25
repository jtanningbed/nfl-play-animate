from fastapi import FastAPI
from app.api.api import router as api_router

app = FastAPI()

# Include the API router
app.include_router(api_router, prefix="/api")

# Additional setup can be done here
