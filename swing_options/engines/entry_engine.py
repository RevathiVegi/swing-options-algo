"""
Simple entry engine — selects a strike using the selector provided via state.
This is intentionally small and pluggable for client replacement.
"""
from typing import Optional, Dict, Any, List

def try_enter_trade(state: Dict[str, Any], cfg: Dict[str, Any], option_chain: List[Dict]) -> Optional[Dict]:
    selector = state.get("selector")
    spot = state.get("spot")
    direction = state.get("direction", "auto")  # 'auto' => choose based on cfg or random in sim
    # choose side: CE for bullish otherwise PE
    side = "CE" if state.get("signal", "BULLISH").upper() == "BULLISH" else "PE"

    strike = selector(
        option_chain,
        spot=spot,
        option_type=side,
        min_open_interest=cfg.get("selection", {}).get("min_open_interest"),
        min_volume=cfg.get("selection", {}).get("min_volume"),
        delta_range=(cfg.get("selection", {}).get("delta_min", 0.3), cfg.get("selection", {}).get("delta_max", 0.7))
    )
    if not strike:
        return None

    qty = cfg.get("lot_size", {}).get("fixed_lots", 1)
    trade = {
        "id": "t-" + str(len(state.get("trades", [])) + 1),
        "symbol": state.get("symbol"),
        "side": side,
        "strike": strike["strike"],
        "entry_price": float(strike.get("premium", 0.0)),
        "quantity": float(qty),
        "fees": float(cfg.get("fees", {}).get("per_trade_fee", 0.0)),
        "status": "OPEN",
    }
    return trade
