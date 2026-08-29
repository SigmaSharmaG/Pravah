import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://harsh:Harsh47@localhost:5433/pravah_db")
    OSRM_URL = os.getenv("OSRM_URL", "http://router.project-osrm.org")

settings = Settings()