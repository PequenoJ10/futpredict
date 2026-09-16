from typing import Dict, Any

def analyze_value(model_prob: float, decimal_odds: float) -> Dict[str, Any]:
    """Calcula la probabilidad implícita, el Edge y el EV (Valor Esperado)."""
    if decimal_odds <= 1.0:
        return {"implied_prob": 0.0, "edge": 0.0, "ev": -1.0, "has_value": False}
    
    implied_prob = 1.0 / decimal_odds
    edge = model_prob - implied_prob
    ev = (model_prob * decimal_odds) - 1.0

    return {
        "model_prob": round(model_prob, 4),
        "implied_prob": round(implied_prob, 4),
        "edge_pct": round(edge * 100, 2),
        "ev_pct": round(ev * 100, 2),
        "has_value": edge > 0.03 and ev > 0.05
    }