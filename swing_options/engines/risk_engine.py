"""
Simple risk checks (daily limits, trade count).
"""
from typing import Dict

def risk_check(state: Dict, cfg: Dict) -> bool:
    # trades per day
    if state.get("trades_today", 0) >= int(cfg.get("risk", {}).get("max_trades_per_day", 4)):
        return False
    # daily loss percent (negative means loss)
    if state.get("todays_loss_pct", 0.0) <= -float(cfg.get("risk", {}).get("max_loss_per_day_pct", 2.0)):
        return False
    return True
