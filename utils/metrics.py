from typing import Any, Optional
import math
import re


def _parse_fy_year(fy_label: Optional[str]) -> Optional[int]:
    if not isinstance(fy_label, str):
        return None
    years = re.findall(r"(19\d{2}|20\d{2})", fy_label)
    if not years:
        return None
    try:
        return int(years[-1])
    except Exception:
        return None


def _safe_number(x: Any) -> Optional[float]:
    return x if isinstance(x, (int, float)) else None


def _stdev(nums: list[float]) -> Optional[float]:
    if len(nums) < 2:
        return None
    mean = sum(nums) / len(nums)
    var = sum((x - mean) ** 2 for x in nums) / (len(nums) - 1)
    return math.sqrt(var)


def compute_metrics(financials: list[dict[str, Any]]) -> dict[str, Any]:
    rows = list(financials or [])
    if not rows:
        return {
            "window_years": 0,
            "fy_range": None,
            "revenue_cagr": None,
            "pat_cagr": None,
            "ebitda_cagr": None,
            "pat_margin": None,
            "ebitda_margin": None,
            "margin_trend_ebitda": None,
            "revenue_volatility": None,
            "debt_to_networth": None,
            "net_debt_to_ebitda": None,
            "cfo_latest": None,
            "cfo_to_pat": None,
            "cfo_positive_years_ratio": None,
            "cfo_cumulative": None,
            "yoy_revenue_growth": [],
        }

    # Sort ascending by parsed FY year when possible; otherwise keep input order
    sortable = [(_parse_fy_year(r.get("fy")), i, r) for i, r in enumerate(rows)]
    if any(y for y, _, _ in sortable):
        sortable.sort(key=lambda t: (9999 if t[0] is None else t[0], t[1]))
        rows = [r for _, _, r in sortable]

    # Use up to last 6 years
    rows = rows[-6:]

    fy_labels = [r.get("fy") for r in rows]
    revenue = [_safe_number(r.get("revenue_cr")) for r in rows]
    pat = [_safe_number(r.get("pat_cr")) for r in rows]
    ebitda = [_safe_number(r.get("ebitda_cr")) for r in rows]
    networth = [_safe_number(r.get("networth_cr")) for r in rows]
    debt = [_safe_number(r.get("debt_cr")) for r in rows]
    cfo = [_safe_number(r.get("cfo_cr")) for r in rows]

    # Basic helpers
    def _cagr(vals: list[Optional[float]]) -> Optional[float]:
        vals_clean = [v for v in vals if isinstance(v, (int, float))]
        if len(vals_clean) < 2:
            return None
        first = None
        # Use first non-null and last non-null while preserving order
        for v in vals:
            if isinstance(v, (int, float)):
                first = v
                break
        last = None
        for v in reversed(vals):
            if isinstance(v, (int, float)):
                last = v
                break
        if first is None or last is None or first <= 0 or last <= 0:
            return None
        n = len(vals) - 1
        try:
            return (last / first) ** (1 / n) - 1
        except Exception:
            return None

    def _margin(numerators: list[Optional[float]], denominators: list[Optional[float]]) -> Optional[float]:
        pairs = [
            (n, d)
            for n, d in zip(numerators, denominators)
            if isinstance(n, (int, float)) and isinstance(d, (int, float)) and d != 0
        ]
        if not pairs:
            return None
        n, d = pairs[-1]
        return n / d

    # YoY revenue growth series
    yoy_growth: list[float] = []
    prev = None
    for v in revenue:
        if prev is not None and isinstance(prev, (int, float)) and isinstance(v, (int, float)) and prev > 0:
            yoy_growth.append((v / prev) - 1)
        prev = v

    # Volatility based on YoY growth
    rev_vol = _stdev(yoy_growth) if len(yoy_growth) >= 2 else None

    # Margin trend (EBITDA margin last - first)
    ebitda_margins_series: list[Optional[float]] = []
    for e, r in zip(ebitda, revenue):
        if isinstance(e, (int, float)) and isinstance(r, (int, float)) and r != 0:
            ebitda_margins_series.append(e / r)
        else:
            ebitda_margins_series.append(None)
    margin_trend = None
    if any(m is not None for m in ebitda_margins_series):
        first_m = next((m for m in ebitda_margins_series if m is not None), None)
        last_m = next((m for m in reversed(ebitda_margins_series) if m is not None), None)
        if first_m is not None and last_m is not None:
            margin_trend = last_m - first_m

    # Latest period figures
    latest_idx = len(rows) - 1
    latest_networth = networth[latest_idx] if isinstance(networth[latest_idx], (int, float)) else None
    latest_debt = debt[latest_idx] if isinstance(debt[latest_idx], (int, float)) else None
    latest_ebitda = ebitda[latest_idx] if isinstance(ebitda[latest_idx], (int, float)) else None
    latest_pat = pat[latest_idx] if isinstance(pat[latest_idx], (int, float)) else None
    latest_cfo = cfo[latest_idx] if isinstance(cfo[latest_idx], (int, float)) else None

    debt_to_networth = None
    if isinstance(latest_debt, (int, float)) and isinstance(latest_networth, (int, float)) and latest_networth != 0:
        debt_to_networth = latest_debt / latest_networth

    net_debt_to_ebitda = None
    if isinstance(latest_debt, (int, float)) and isinstance(latest_ebitda, (int, float)) and latest_ebitda != 0:
        net_debt_to_ebitda = latest_debt / latest_ebitda

    cfo_to_pat = None
    if isinstance(latest_cfo, (int, float)) and isinstance(latest_pat, (int, float)) and latest_pat != 0:
        cfo_to_pat = latest_cfo / latest_pat

    cfo_pos_ratio = None
    cfo_clean = [v for v in cfo if isinstance(v, (int, float))]
    if cfo_clean:
        pos = sum(1 for v in cfo_clean if v > 0)
        cfo_pos_ratio = pos / len(cfo_clean)

    cfo_cum = sum(v for v in cfo_clean) if cfo_clean else None

    metrics = {
        "window_years": len(rows),
        "fy_range": [fy_labels[0], fy_labels[-1]] if fy_labels else None,
        "revenue_cagr": _cagr(revenue),
        "pat_cagr": _cagr(pat),
        "ebitda_cagr": _cagr(ebitda),
        "pat_margin": _margin(pat, revenue),
        "ebitda_margin": _margin(ebitda, revenue),
        "margin_trend_ebitda": margin_trend,
        "revenue_volatility": rev_vol,
        "debt_to_networth": debt_to_networth,
        "net_debt_to_ebitda": net_debt_to_ebitda,
        "cfo_latest": latest_cfo,
        "cfo_to_pat": cfo_to_pat,
        "cfo_positive_years_ratio": cfo_pos_ratio,
        "cfo_cumulative": cfo_cum,
        "yoy_revenue_growth": yoy_growth,
    }
    return metrics 