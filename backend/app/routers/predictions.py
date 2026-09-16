from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
import math
from app.database import get_db
from app.models.prediction import PredictionHistoryModel

router = APIRouter(prefix="/predictions", tags=["Predictions"])

TEAM_STATS = {
    "Real Madrid": {"attack": 1.95, "defense": 0.70},
    "Barcelona": {"attack": 1.90, "defense": 0.75},
    "Atlético de Madrid": {"attack": 1.50, "defense": 0.75},
    "Athletic Club": {"attack": 1.35, "defense": 0.90},
    "Real Sociedad": {"attack": 1.25, "defense": 0.95},
    "Villarreal": {"attack": 1.40, "defense": 1.15},
    "Real Betis": {"attack": 1.20, "defense": 1.05},
    "Sevilla": {"attack": 1.15, "defense": 1.20},
    "Getafe": {"attack": 0.90, "defense": 1.00},
    "Osasuna": {"attack": 1.05, "defense": 1.15},
    "Rayo Vallecano": {"attack": 1.00, "defense": 1.10},
    "Alavés": {"attack": 0.95, "defense": 1.20},
    "Valencia": {"attack": 1.00, "defense": 1.15},
    "Celta": {"attack": 1.10, "defense": 1.25},
    "Mallorca": {"attack": 0.90, "defense": 1.10},
    "Espanyol": {"attack": 0.95, "defense": 1.30},
    "Elche": {"attack": 0.85, "defense": 1.35},
    "Girona": {"attack": 1.30, "defense": 1.10}
}

DEFAULT_STATS = {"attack": 1.05, "defense": 1.10}
LEAGUE_AVG_GOALS = 1.35

def poisson_probability(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

@router.post("/")
def generate_prediction(
    home_team: str = Query(...), 
    away_team: str = Query(...), 
    db: Session = Depends(get_db)
):
    home = next((v for k, v in TEAM_STATS.items() if k.lower() in home_team.lower()), DEFAULT_STATS)
    away = next((v for k, v in TEAM_STATS.items() if k.lower() in away_team.lower()), DEFAULT_STATS)

    home_xg = round((home["attack"] * away["defense"] * LEAGUE_AVG_GOALS) * 1.10, 2)
    away_xg = round(away["attack"] * home["defense"] * LEAGUE_AVG_GOALS, 2)

    home_win, draw, away_win = 0.0, 0.0, 0.0
    for i in range(7):
        for j in range(7):
            p = poisson_probability(home_xg, i) * poisson_probability(away_xg, j)
            if i > j: home_win += p
            elif i == j: draw += p
            else: away_win += p

    total_p = home_win + draw + away_win
    h_prob = round((home_win / total_p) * 100, 1)
    d_prob = round((draw / total_p) * 100, 1)
    a_prob = round((away_win / total_p) * 100, 1)

    if h_prob > a_prob and h_prob > d_prob:
        winner = f"Victoria de {home_team}"
    elif a_prob > h_prob and a_prob > d_prob:
        winner = f"Victoria de {away_team}"
    else:
        winner = "Empate muy probable"

    # Guardar en la base de datos PostgreSQL
    db_prediction = PredictionHistoryModel(
        home_team=home_team,
        away_team=away_team,
        prediction=winner,
        expected_home_goals=home_xg,
        expected_away_goals=away_xg,
        home_win_probability=h_prob,
        draw_probability=d_prob,
        away_win_probability=a_prob
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return {
        "id": db_prediction.id,
        "prediction": winner,
        "expected_home_goals": home_xg,
        "expected_away_goals": away_xg,
        "home_win_probability": h_prob,
        "draw_probability": d_prob,
        "away_win_probability": a_prob,
        "created_at": db_prediction.created_at
    }

@router.get("/history")
def get_prediction_history(db: Session = Depends(get_db)):
    return db.query(PredictionHistoryModel).order_by(PredictionHistoryModel.created_at.desc()).all()