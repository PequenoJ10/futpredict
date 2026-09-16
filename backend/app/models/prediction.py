from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class PredictionHistoryModel(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, index=True)
    away_team = Column(String, index=True)
    prediction = Column(String)
    expected_home_goals = Column(Float)
    expected_away_goals = Column(Float)
    home_win_probability = Column(Float)
    draw_probability = Column(Float)
    away_win_probability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)