from typing import Any, Optional


def compute_metrics(financials: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [r for r in financials if r.get("revenue_cr") is not None]
    rows = rows[-3:] if len(rows) >= 3 else rows
    revenue = [r.get("revenue_cr") for r in rows if isinstance(r.get("revenue_cr"), (int, float))]
    pat = [r.get("pat_cr") for r in rows if isinstance(r.get("pat_cr"), (int, float))]
    ebitda = [r.get("ebitda_cr") for r in rows if isinstance(r.get("ebitda_cr"), (int, float))]

    def cagr(vals: list[float]) -> Optional[float]:
        if len(vals) < 2:
            return None
        first, last = vals[0], vals[-1]
        n = len(vals) - 1
        if first is None or first <= 0 or last is None or last <= 0:
            return None
        try:
            return (last / first) ** (1 / n) - 1
        except Exception:
            return None

    def margin(numerators: list[Optional[float]], denominators: list[Optional[float]]) -> Optional[float]:
        pairs = [
            (n, d)
            for n, d in zip(numerators, denominators)
            if isinstance(n, (int, float)) and isinstance(d, (int, float)) and d != 0
        ]
        if not pairs:
            return None
        n, d = pairs[-1]
        return n / d

    revenue_vals = [v for v in revenue if isinstance(v, (int, float))]
    pat_vals = [v for v in pat if isinstance(v, (int, float))]
    ebitda_vals = [v for v in ebitda if isinstance(v, (int, float))]

    metrics = {
        "revenue_cagr_3y": cagr(revenue_vals),
        "pat_margin": margin(pat_vals, revenue_vals) if revenue_vals else None,
        "ebitda_margin": margin(ebitda_vals, revenue_vals) if revenue_vals else None,
    }
    return metrics 