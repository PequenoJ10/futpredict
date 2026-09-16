from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.match import Match
from app.services.sports_api import SportsAPIService

router = APIRouter(prefix="/api/matches", tags=["Matches"])
api_service = SportsAPIService()

@router.get("/")
def get_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()

@router.post("/sync")
def sync_matches(league_code: str = "PD", db: Session = Depends(get_db)):
    try:
        count = api_service.sync_league_matches(db, league_code)
        return {"message": "Sincronización exitosa", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))