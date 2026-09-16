import math
import numpy as np
from typing import Dict, Any, List

def poisson_probability(k: int, lambda_val: float) -> float:
    if lambda_val <= 0: return 0.0
    return (math.pow(lambda_val, k) * math.exp(-lambda_val)) / math.factorial(k)

def calculate_expected_goals(
    home_att: float, home_def: float, 
    away_att: float, away_def: float, 
    league_home_avg: float = 1.45, league_away_avg: float = 1.15,
    h2h_avg_goals: float = 2.5, h2h_weight: float = 0.05
) -> tuple[float, float]:
    """Cálculo estricto de xG aplicando fuerza ofensiva/defensiva y ventaja de localía."""
    home_attack_factor = home_att / league_home_avg if league_home_avg else 1.0
    away_defense_factor = away_def / league_away_avg if league_away_avg else 1.0
    
    away_attack_factor = away_att / league_away_avg if league_away_avg else 1.0
    home_defense_factor = home_def / league_home_avg if league_home_avg else 1.0

    xg_home = league_home_avg * home_attack_factor * away_defense_factor
    xg_away = league_away_avg * away_attack_factor * home_defense_factor

    # Ajuste por H2H con peso configurable reducido
    xg_home = xg_home * (1 - h2h_weight) + (h2h_avg_goals * 0.52) * h2h_weight
    xg_away = xg_away * (1 - h2h_weight) + (h2h_avg_goals * 0.48) * h2h_weight

    return round(xg_home, 2), round(xg_away, 2)

def generate_score_matrix(xg_home: float, xg_away: float, max_goals: int = 6) -> np.ndarray:
    matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            matrix[i, j] = poisson_probability(i, xg_home) * poisson_probability(j, xg_away)
    return matrix