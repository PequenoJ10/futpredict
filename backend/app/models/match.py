from sqlalchemy import Column, Integer, String
from app.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    match_date = Column(String, nullable=True)
    status = Column(String, default="TIMED")