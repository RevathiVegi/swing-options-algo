"""
Simple exit engine — exits based on percent target/stop or EOD.
"""
from typing import Dict, Any

def should_exit(trade: Dict[str, Any], mark_price: float, now_time: str, cfg: Dict[str, Any]) -> bool:
    entry = float(trade.get("entry_price", 0.0))
    if entry == 0:
        return True
    pct_move = ((float(mark_price) - entry) / entry) * 100.0
    # EOD
    if cfg.get("exit", {}).get("eod_exit_enabled") and now_time >= cfg.get("exit", {}).get("eod_time", "15:25"):
        return True
    if pct_move >= cfg.get("exit", {}).get("target_pct", 5):
        return True
    if pct_move <= -cfg.get("exit", {}).get("stoploss_pct", 20):
        return True
    return False
