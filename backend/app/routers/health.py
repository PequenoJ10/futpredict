from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(tags=["Health"])

@router.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    """Verifica que el servicio y la conexión a PostgreSQL funcionen correctamente."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

    return {
        "status": "online",
        "database": db_status,
        "engine": "FastAPI + SQLAlchemy"
    }