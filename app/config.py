from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db = os.getenv("DB_NAME")
hostname = os.getenv("DB_HOSTNAME")
DATABASE_URL = f"postgresql://{user}:{password}@{hostname}/{db}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
