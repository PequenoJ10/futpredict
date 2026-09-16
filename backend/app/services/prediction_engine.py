import numpy as np
from app.config import settings
from app.services.poisson import calculate_expected_goals, generate_score_matrix
from app.services.value import analyze_value

def generate_prediction(match_data: dict) -> dict:
    home = match_data.get("local", {})
    away = match_data.get("visitante", {})
    odds = match_data.get("odds", {})

    # Calidad de datos y nivel de confianza
    samples = home.get("matches", 0) + away.get("matches", 0)
    data_quality = 92.0 if samples >= 16 else (65.0 if samples >= 8 else 40.0)
    
    if data_quality < 50.0:
        confianza = "BAJA (⚠️ DATOS INSUFICIENTES)"
    elif data_quality < 80.0:
        confianza = "MEDIA"
    else:
        confianza = "ALTA"

    xg_home, xg_away = calculate_expected_goals(
        home_att=home.get("goals_for_home", 1.4),
        home_def=home.get("goals_against_home", 1.0),
        away_att=away.get("goals_for_away", 1.2),
        away_def=away.get("goals_against_away", 1.2),
        h2h_weight=settings.WEIGHTS["h2h"]
    )

    matrix = generate_score_matrix(xg_home, xg_away)
    
    p_home = float(np.sum(np.tril(matrix, -1)))
    p_draw = float(np.sum(np.diag(matrix)))
    p_away = float(np.sum(np.triu(matrix, 1)))

    btts_si = float(np.sum(matrix[1:, 1:]))
    btts_no = 1.0 - btts_si

    over_1_5 = float(np.sum([matrix[i, j] for i in range(7) for j in range(7) if i + j > 1.5]))
    over_2_5 = float(np.sum([matrix[i, j] for i in range(7) for j in range(7) if i + j > 2.5]))
    over_3_5 = float(np.sum([matrix[i, j] for i in range(7) for j in range(7) if i + j > 3.5]))

    # Marcadores probables
    scores = []
    for i in range(6):
        for j in range(6):
            scores.append({"score": f"{i}-{j}", "prob": float(matrix[i, j])})
    scores.sort(key=lambda x: x["prob"], reverse=True)

    # Valor estadístico vs cuotas
    value_analysis = {}
    if odds:
        value_analysis["local"] = analyze_value(p_home, odds.get("local", 0))
        value_analysis["empate"] = analyze_value(p_draw, odds.get("empate", 0))
        value_analysis["visitante"] = analyze_value(p_away, odds.get("visitante", 0))

    return {
        "match_id": match_data.get("id"),
        "probabilidad_local": round(p_home, 4),
        "probabilidad_empate": round(p_draw, 4),
        "probabilidad_visitante": round(p_away, 4),
        "goles_esperados_local": xg_home,
        "goles_esperados_visitante": xg_away,
        "over_1_5": round(over_1_5, 4),
        "over_2_5": round(over_2_5, 4),
        "over_3_5": round(over_3_5, 4),
        "under_1_5": round(1.0 - over_1_5, 4),
        "under_2_5": round(1.0 - over_2_5, 4),
        "btts_si": round(btts_si, 4),
        "btts_no": round(btts_no, 4),
        "corners_expected": round(home.get("corners_avg", 5.0) + away.get("corners_avg", 5.0), 1),
        "cards_expected": round(home.get("cards_avg", 2.0) + away.get("cards_avg", 2.0), 1),
        "marcador_probable": scores[0]["score"],
        "top_marcadores": scores[:5],
        "nivel_confianza": confianza,
        "calidad_datos_pct": data_quality,
        "valor_estadistico": value_analysis,
        "version_del_modelo": settings.MODEL_VERSION
    }