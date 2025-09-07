from typing import Any, Optional


class DecisionEngine:
    def __init__(
        self,
        weight_growth: float = 0.30,
        weight_profitability: float = 0.25,
        weight_cashflow: float = 0.20,
        weight_leverage: float = 0.15,
        weight_volatility: float = 0.10,
    ) -> None:
        self.weight_growth = weight_growth
        self.weight_profitability = weight_profitability
        self.weight_cashflow = weight_cashflow
        self.weight_leverage = weight_leverage
        self.weight_volatility = weight_volatility

    def _score_growth(self, m: dict[str, Any], reasons: list[str]) -> float:
        score = 0.0
        cagr = m.get("revenue_cagr")
        if isinstance(cagr, (int, float)):
            if cagr >= 0.20:
                score += 100; reasons.append("Strong revenue CAGR")
            elif cagr >= 0.10:
                score += 70; reasons.append("Moderate revenue CAGR")
            elif cagr > 0:
                score += 40; reasons.append("Low revenue CAGR")
            else:
                score += 15; reasons.append("Declining revenue")
        else:
            reasons.append("Revenue CAGR unavailable")
            score += 25

        # Bonus for EBITDA CAGR if available
        ecagr = m.get("ebitda_cagr")
        if isinstance(ecagr, (int, float)) and ecagr > 0.10:
            score += 10; reasons.append("EBITDA CAGR supportive")
        return min(score, 100)

    def _score_profitability(self, m: dict[str, Any], reasons: list[str]) -> float:
        score = 0.0
        em = m.get("ebitda_margin")
        pm = m.get("pat_margin")
        if isinstance(em, (int, float)):
            if em >= 0.20:
                score += 55; reasons.append("Strong EBITDA margin")
            elif em >= 0.12:
                score += 40; reasons.append("Moderate EBITDA margin")
            elif em > 0.05:
                score += 25; reasons.append("Thin EBITDA margin")
            else:
                score += 10; reasons.append("Weak EBITDA margin")
        else:
            score += 20; reasons.append("EBITDA margin unavailable")
        if isinstance(pm, (int, float)):
            if pm >= 0.12:
                score += 35; reasons.append("Healthy PAT margin")
            elif pm >= 0.07:
                score += 25; reasons.append("Moderate PAT margin")
            elif pm > 0:
                score += 15; reasons.append("Thin PAT margin")
            else:
                score += 5; reasons.append("Negative PAT")
        else:
            score += 15; reasons.append("PAT margin unavailable")

        # Margin trend bonus
        mt = m.get("margin_trend_ebitda")
        if isinstance(mt, (int, float)) and mt > 0:
            score += 10; reasons.append("Improving EBITDA margin trend")
        return min(score, 100)

    def _score_cashflow(self, m: dict[str, Any], reasons: list[str]) -> float:
        score = 0.0
        cfo_latest = m.get("cfo_latest")
        cfo_to_pat = m.get("cfo_to_pat")
        cfo_pos_ratio = m.get("cfo_positive_years_ratio")
        if isinstance(cfo_latest, (int, float)) and cfo_latest > 0:
            score += 45; reasons.append("Latest CFO positive")
        elif isinstance(cfo_latest, (int, float)):
            score += 15; reasons.append("Latest CFO negative")
        else:
            score += 25; reasons.append("CFO data unavailable")
        if isinstance(cfo_to_pat, (int, float)):
            if cfo_to_pat >= 0.9:
                score += 35; reasons.append("Strong cash conversion")
            elif cfo_to_pat >= 0.5:
                score += 25; reasons.append("Moderate cash conversion")
            elif cfo_to_pat > 0:
                score += 15; reasons.append("Weak cash conversion")
            else:
                score += 5; reasons.append("Poor cash conversion")
        if isinstance(cfo_pos_ratio, (int, float)):
            if cfo_pos_ratio >= 0.66:
                score += 20; reasons.append("Consistently positive CFO")
            elif cfo_pos_ratio >= 0.33:
                score += 10; reasons.append("Occasionally positive CFO")
            else:
                score += 5; reasons.append("Mostly negative CFO")
        return min(score, 100)

    def _score_leverage(self, m: dict[str, Any], reasons: list[str]) -> float:
        score = 0.0
        dnw = m.get("debt_to_networth")
        nde = m.get("net_debt_to_ebitda")
        if isinstance(dnw, (int, float)):
            if dnw <= 0.5:
                score += 50; reasons.append("Low leverage vs net worth")
            elif dnw <= 1.0:
                score += 35; reasons.append("Moderate leverage vs net worth")
            elif dnw <= 2.0:
                score += 20; reasons.append("High leverage vs net worth")
            else:
                score += 10; reasons.append("Very high leverage")
        else:
            score += 25; reasons.append("Leverage (DNW) unavailable")
        if isinstance(nde, (int, float)):
            if nde <= 1.0:
                score += 50; reasons.append("Low net debt to EBITDA")
            elif nde <= 3.0:
                score += 35; reasons.append("Moderate net debt to EBITDA")
            elif nde <= 5.0:
                score += 20; reasons.append("High net debt to EBITDA")
            else:
                score += 10; reasons.append("Very high net debt to EBITDA")
        else:
            score += 25; reasons.append("Net debt to EBITDA unavailable")
        return min(score, 100)

    def _score_volatility(self, m: dict[str, Any], reasons: list[str]) -> float:
        score = 0.0
        vol = m.get("revenue_volatility")
        if isinstance(vol, (int, float)):
            if vol <= 0.10:
                score += 100; reasons.append("Low revenue volatility")
            elif vol <= 0.20:
                score += 70; reasons.append("Moderate revenue volatility")
            else:
                score += 35; reasons.append("High revenue volatility")
        else:
            score += 50; reasons.append("Volatility unavailable")
        return min(score, 100)

    def decide(self, metrics: dict[str, Any]) -> dict[str, Any]:
        reasons: list[str] = []
        sg = self._score_growth(metrics, reasons)
        sp = self._score_profitability(metrics, reasons)
        sc = self._score_cashflow(metrics, reasons)
        sl = self._score_leverage(metrics, reasons)
        sv = self._score_volatility(metrics, reasons)

        score = (
            sg * self.weight_growth
            + sp * self.weight_profitability
            + sc * self.weight_cashflow
            + sl * self.weight_leverage
            + sv * self.weight_volatility
        )

        label = "Avoid"
        if score >= 70:
            label = "Apply"
        elif score >= 55:
            label = "Neutral"

        # Confidence: tighter banding around thresholds reduces confidence
        dist = min(abs(score - 70), abs(score - 55)) / 15.0
        confidence = max(0.4, min(0.95, 1.0 - dist))

        return {
            "label": label,
            "score": round(score, 2),
            "confidence": round(confidence, 2),
            "reasons": reasons,
        } 