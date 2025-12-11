from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def is_itm(record: Dict, spot: float) -> bool:
    st = float(record["strike"])
    typ = record["option_type"].upper()
    if typ in ("CE", "CALL"):
        return st < spot
    if typ in ("PE", "PUT"):
        return st > spot
    raise ValueError(f"Unknown option_type {typ}")

def select_itm_strike(
    strikes: List[Dict],
    spot: float,
    option_type: str,
    prefer_nearest: bool = True,
    delta_range: Optional[Tuple[float, float]] = (0.30, 0.70),
    min_open_interest: Optional[int] = None,
    min_volume: Optional[int] = None,
    max_premium: Optional[float] = None
) -> Optional[Dict]:
    if not isinstance(spot, (int, float)):
        raise ValueError("spot must be numeric")

    option_type = option_type.upper()

    candidates = [r for r in strikes if r.get("option_type", "").upper() == option_type]
    itm = [r for r in candidates if is_itm(r, spot)]

    if not itm:
        logger.info("No ITM strikes found for %s at spot=%.2f", option_type, spot)
        return None

    def passes_filters(r):
        if min_open_interest is not None and int(r.get("open_interest", 0)) < min_open_interest:
            return False
        if min_volume is not None and int(r.get("volume", 0)) < min_volume:
            return False
        if max_premium is not None and float(r.get("premium", 0.0)) > max_premium:
            return False
        if delta_range is not None:
            d = abs(float(r.get("delta", 0.0)))
            if d < delta_range[0] or d > delta_range[1]:
                return False
        return True

    filtered = [r for r in itm if passes_filters(r)]
    if not filtered:
        logger.info("No strikes passed filters; falling back to nearest ITM only")
        filtered = itm

    # ranking: nearest first, highest OI second, highest volume third
    def score(r):
        strike_diff = abs(float(r["strike"]) - spot)
        oi = -int(r.get("open_interest", 0))
        vol = -int(r.get("volume", 0))
        return (strike_diff, oi, vol)

    best = min(filtered, key=score)
    logger.debug(
        "Selected strike=%s diff=%.2f oi=%s vol=%s",
        best["strike"],
        abs(float(best["strike"]) - spot),
        best.get("open_interest"),
        best.get("volume")
    )
    return best
