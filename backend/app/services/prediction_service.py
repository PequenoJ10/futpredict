# Fuerza de ataque y defensa por equipo en las principales ligas europeas
TEAM_RATINGS = {
    # LaLiga (España)
    "Real Madrid CF": {"attack": 1.95, "defense": 0.70},
    "FC Barcelona": {"attack": 1.90, "defense": 0.75},
    "Club Atlético de Madrid": {"attack": 1.50, "defense": 0.80},
    "Sevilla FC": {"attack": 1.10, "defense": 1.25},
    "Real Betis Balompié": {"attack": 1.25, "defense": 1.15},
    "Villarreal CF": {"attack": 1.35, "defense": 1.10},
    "Athletic Club": {"attack": 1.30, "defense": 0.90},
    "Girona FC": {"attack": 1.40, "defense": 1.15},
    "Real Sociedad de Fútbol": {"attack": 1.30, "defense": 0.95},

    # Premier League (Inglaterra)
    "Manchester City FC": {"attack": 2.05, "defense": 0.65},
    "Arsenal FC": {"attack": 1.90, "defense": 0.70},
    "Liverpool FC": {"attack": 1.95, "defense": 0.75},
    "Chelsea FC": {"attack": 1.60, "defense": 1.00},
    "Manchester United FC": {"attack": 1.45, "defense": 1.15},
    "Tottenham Hotspur FC": {"attack": 1.65, "defense": 1.10},
    "Aston Villa FC": {"attack": 1.55, "defense": 1.05},

    # Serie A (Italia)
    "FC Internazionale Milano": {"attack": 1.85, "defense": 0.70},
    "AC Milan": {"attack": 1.65, "defense": 0.90},
    "Juventus FC": {"attack": 1.55, "defense": 0.80},
    "SSC Napoli": {"attack": 1.60, "defense": 0.85},

    # Bundesliga (Alemania) & Ligue 1 (Francia)
    "FC Bayern München": {"attack": 2.00, "defense": 0.70},
    "Bayer 04 Leverkusen": {"attack": 1.85, "defense": 0.80},
    "Borussia Dortmund": {"attack": 1.70, "defense": 0.95},
    "Paris Saint-Germain FC": {"attack": 1.95, "defense": 0.75}
}

DEFAULT_RATING = {"attack": 1.00, "defense": 1.20}
LEAGUE_AVG_GOALS = 1.35

class PredictionService:
    def predict_match(self, home_team: str, away_team: str):
        home_stats = TEAM_RATINGS.get(home_team, DEFAULT_RATING)
        away_stats = TEAM_RATINGS.get(away_team, DEFAULT_RATING)

        # xG: (Ataque Local * Defensa Visitante * Promedio) + Factor Localía (+10%)
        home_xg = round(home_stats["attack"] * away_stats["defense"] * LEAGUE_AVG_GOALS * 1.10 / 1.3, 2)
        away_xg = round(away_stats["attack"] * home_stats["defense"] * LEAGUE_AVG_GOALS / 1.3, 2)

        # Córners estimados
        total_corners = round((home_stats["attack"] + away_stats["attack"]) * 4.3, 1)

        diff = home_xg - away_xg
        if diff > 0.35:
            winner = f"Gana {home_team}"
            conf = min(0.88, round(0.52 + (diff * 0.18), 2))
        elif diff < -0.35:
            winner = f"Gana {away_team}"
            conf = min(0.88, round(0.52 + (abs(diff) * 0.18), 2))
        else:
            winner = "Empate / Partido Parejo"
            conf = round(0.42 + (abs(diff) * 0.10), 2)

        return {
            "predicted_winner": winner,
            "confidence": conf,
            "home_exp_goals": home_xg,
            "away_exp_goals": away_xg,
            "total_exp_corners": total_corners
        }