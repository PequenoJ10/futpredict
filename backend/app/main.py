from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

import app.models.match
import app.models.prediction

from app.routers import health, matches, predictions

# Crear automáticamente las tablas en la base de datos (incluyendo el nuevo campo match_date)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FutPredict API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(matches.router)
app.include_router(predictions.router)

@app.get("/")
def root():
    return {"message": "FutPredict API Online"}