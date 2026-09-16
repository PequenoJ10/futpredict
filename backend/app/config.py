from pydantic_settings import BaseSettings
from typing import Dict, Any

class Settings(BaseSettings):
    PROJECT_NAME: str = "FutPredict API"
    VERSION: str = "1.0.0"
    MODEL_VERSION: str = "poisson-v1.0"
    
    # Base de Datos
    DATABASE_URL: str = "postgresql://futpredict:futpredict_pass@localhost:5432/futpredict_db"
    
    # API Deportiva
    SPORTS_API_KEY: str = ""
    SPORTS_API_URL: str = "https://api.football-data.org/v4"
    SPORTS_PROVIDER: str = "demo"  # "demo" o "external"
    
    # Pesos del modelo estadístico (Configurables sin alterar código)
    WEIGHTS: Dict[str, float] = {
        "recent_form": 0.25,
        "home_away_perf": 0.25,
        "attack": 0.15,
        "defense": 0.15,
        "league_avg": 0.10,
        "h2h": 0.05,
        "other": 0.05
    }

    class Config:
        env_file = ".env"

settings = Settings()