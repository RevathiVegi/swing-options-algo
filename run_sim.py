# run_sim.py
"""
Lightweight trade bookkeeping and PnL utilities used by the simulator.
No external dependencies.
"""

from typing import Dict, Any, Optional, List
import logging
import math
import time
import uuid

logger = logging.getLogger(__name__)


def ensure_trade_pnl(trade: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure trade contains realized_pnl, unrealized_pnl and net_pnl keys.
    Convention: quantity > 0 means LONG (profit = (exit - entry) * qty).
    """
    fees = float(trade.get("fees", 0.0))
    qty = float(trade.get("quantity", 0.0))
    entry = trade.get("entry_price")
    exitp = trade.get("exit_price")
    mark = trade.get("mark_price", exitp if exitp is not None else entry)

    def pnl_for_prices(open_p, close_p):
        if open_p is None or close_p is None:
            return 0.0
        return (float(close_p) - float(open_p)) * qty

    realized_pnl = pnl_for_prices(entry, exitp) if exitp is not None else 0.0
    unrealized_pnl = pnl_for_prices(entry, mark) if exitp is None else 0.0
    net_pnl = realized_pnl + unrealized_pnl - fees

    try:
        realized_pnl = float(round(realized_pnl, 6))
        unrealized_pnl = float(round(unrealized_pnl, 6))
        net_pnl = float(round(net_pnl, 6))
    except Exception:
        realized_pnl = unrealized_pnl = net_pnl = 0.0

    trade["realized_pnl"] = realized_pnl
    trade["unrealized_pnl"] = unrealized_pnl
    trade["net_pnl"] = net_pnl
    trade["fees"] = fees

    if math.isinf(net_pnl) or math.isnan(net_pnl):
        logger.warning("Computed NaN/Inf PnL for trade %s — zeroing values", trade.get("id"))
        trade["realized_pnl"] = 0.0
        trade["unrealized_pnl"] = 0.0
        trade["net_pnl"] = 0.0

    return trade


class TradeBook:
    """In-memory trade book with simple open/close/update operations."""

    def __init__(self):
        self.trades: Dict[str, Dict[str, Any]] = {}

    def open_trade(
        self,
        symbol: str,
        strike: float,
        option_type: str,
        quantity: float,
        entry_price: float,
        fees: float = 0.0,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        tid = str(uuid.uuid4())
        trade = {
            "id": tid,
            "symbol": symbol,
            "strike": float(strike),
            "option_type": option_type,
            "entry_price": float(entry_price),
            "exit_price": None,
            "quantity": float(quantity),
            "fees": float(fees),
            "mark_price": float(entry_price),
            "opened_at": time.time(),
            "closed_at": None,
            "meta": meta or {},
        }
        ensure_trade_pnl(trade)
        self.trades[tid] = trade
        logger.info("Opened trade %s %s %s qty=%s entry=%.2f", tid, symbol, option_type, quantity, entry_price)
        return trade

    def close_trade(self, trade_id: str, exit_price: float, close_time: Optional[float] = None) -> Dict[str, Any]:
        if trade_id not in self.trades:
            raise KeyError("Trade id not found: %s" % trade_id)
        trade = self.trades[trade_id]
        trade["exit_price"] = float(exit_price)
        trade["closed_at"] = close_time or time.time()
        trade["mark_price"] = trade["exit_price"]
        ensure_trade_pnl(trade)
        logger.info(
            "Closed trade %s exit=%.2f realized=%.2f net=%.2f", trade_id, trade["exit_price"], trade["realized_pnl"], trade["net_pnl"]
        )
        return trade

    def update_mark(self, trade_id: str, mark_price: float) -> Dict[str, Any]:
        if trade_id not in self.trades:
            raise KeyError("Trade id not found: %s" % trade_id)
        trade = self.trades[trade_id]
        if trade["exit_price"] is None:
            trade["mark_price"] = float(mark_price)
            ensure_trade_pnl(trade)
        return trade

    def open_trades(self) -> List[Dict[str, Any]]:
        return [t for t in self.trades.values() if t["exit_price"] is None]

    def closed_trades(self) -> List[Dict[str, Any]]:
        return [t for t in self.trades.values() if t["exit_price"] is not None]

    def summary(self) -> Dict[str, Any]:
        closed = self.closed_trades()
        total_realized = sum(t.get("realized_pnl", 0.0) for t in closed)
        total_fees = sum(t.get("fees", 0.0) for t in self.trades.values())
        net = sum(t.get("net_pnl", 0.0) for t in self.trades.values() if t.get("exit_price") is not None)
        return {
            "count_open": len(self.open_trades()),
            "count_closed": len(closed),
            "total_realized": round(total_realized, 6),
            "total_fees": round(total_fees, 6),
            "net": round(net, 6),
        }
