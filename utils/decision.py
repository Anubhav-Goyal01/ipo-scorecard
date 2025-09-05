from typing import Any


def simple_decision(metrics: dict[str, Any]) -> dict[str, Any]:
    score = 0.0
    reasons: list[str] = []

    cagr = metrics.get("revenue_cagr_3y")
    if isinstance(cagr, (int, float)):
        if cagr >= 0.2:
            score += 35
            reasons.append("Strong revenue CAGR")
        elif cagr >= 0.1:
            score += 20
            reasons.append("Moderate revenue CAGR")
        else:
            score += 10
            reasons.append("Low revenue CAGR")
    else:
        reasons.append("Insufficient data for CAGR")

    pm = metrics.get("pat_margin")
    if isinstance(pm, (int, float)):
        if pm >= 0.12:
            score += 25
            reasons.append("Healthy PAT margin")
        elif pm >= 0.07:
            score += 15
            reasons.append("Moderate PAT margin")
        else:
            score += 5
            reasons.append("Thin PAT margin")
    else:
        reasons.append("PAT margin unavailable")

    em = metrics.get("ebitda_margin")
    if isinstance(em, (int, float)):
        if em >= 0.18:
            score += 20
            reasons.append("Good EBITDA margin")
        elif em >= 0.1:
            score += 12
            reasons.append("Moderate EBITDA margin")
        else:
            score += 5
            reasons.append("Thin EBITDA margin")
    else:
        reasons.append("EBITDA margin unavailable")

    score += 10

    label = "Avoid"
    if score >= 70:
        label = "Apply"
    elif score >= 55:
        label = "Neutral"

    dist = min(abs(score - 70), abs(score - 55)) / 15.0
    confidence = max(0.4, min(0.95, 1.0 - dist))

    return {"label": label, "score": round(score, 2), "confidence": round(confidence, 2), "reasons": reasons} 