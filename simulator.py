# simulator.py
"""
Self-contained simulator that uses the lightweight run_sim.TradeBook and an internal mock feed.
No external data files required.
"""

import argparse
import logging
import random
import time
from typing import Dict, List

# try to load yaml if available, otherwise fallback to defaults
try:
    import yaml  # type: ignore
    YAML_AVAILABLE = True
except Exception:
    YAML_AVAILABLE = False

from run_sim import TradeBook

logger = logging.getLogger(__name__)


class MockFeed:
    """Generates a spot and a list of option strikes with simple metadata."""

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

    def snapshot(self, symbol: str) -> Dict:
        base = 15000 + (abs(hash(symbol)) % 1000)  # deterministic-ish base
        spot = float(base + random.randint(-100, 100))
        strikes = []
        # generate strikes every 50 between spot-500 and spot+500
        for s in range(int(spot) - 500, int(spot) + 501, 50):
            for typ in ("CE", "PE"):
                distance = abs(s - spot)
                premium = max(0.5, distance / 15.0 + random.uniform(-1.0, 1.0))
                # delta toward 0.5 at ATM, smaller away
                delta_base = max(0.01, min(0.99, 0.5 - (distance / 1000.0)))
                signed_delta = delta_base if typ == "CE" else -delta_base
                oi = random.randint(5, 2000)
                vol = random.randint(0, 500)
                strikes.append(
                    {
                        "strike": float(s),
                        "option_type": typ,
                        "delta": signed_delta,
                        "open_interest": oi,
                        "volume": vol,
                        "premium": round(premium, 2),
                    }
                )
        return {"spot": spot, "strikes": strikes}


def select_itm_strike_simple(strikes: List[Dict], spot: float, option_type: str):
    """
    A minimal fallback selector in case swing_options.strike_selector isn't present.
    Selects nearest ITM strike for CE/PE, prefers higher OI on tie.
    """
    option_type = option_type.upper()

    def is_itm(r):
        st = float(r["strike"])
        if option_type == "CE":
            return st < spot
        return st > spot

    cand = [r for r in strikes if r.get("option_type", "").upper() == option_type and is_itm(r)]
    if not cand:
        return None
    best = min(cand, key=lambda r: (abs(float(r["strike"]) - spot), -int(r.get("open_interest", 0)), -int(r.get("volume", 0))))
    return best


class SimpleSim:
    def __init__(self, cfg: Dict):
        self.cfg = cfg
        self.feed = MockFeed(seed=cfg.get("seed"))
        self.book = TradeBook()
        # allow external selector if package exists
        try:
            from swing_options.strike_selector import select_itm_strike as external_selector  # type: ignore
            self.selector = external_selector
            logger.info("Using swing_options.strike_selector.select_itm_strike")
        except Exception:
            self.selector = select_itm_strike_simple
            logger.info("Using internal simple selector (no external module)")

        sel = cfg.get("selectors", {})
        self.delta_range = tuple(sel.get("delta_range", (0.30, 0.70)))
        self.min_oi = sel.get("min_open_interest", 10)
        self.min_vol = sel.get("min_volume", 0)

    def run_for_symbol(self, symbol: str):
        snap = self.feed.snapshot(symbol)
        spot = snap["spot"]
        strikes = snap["strikes"]
        logger.info("Snapshot for %s: spot=%.2f strikes=%d", symbol, spot, len(strikes))

        direction = self.cfg.get("direction", "random")
        if direction == "random":
            direction = random.choice(["buy_call", "buy_put"])

        want_call = direction == "buy_call"
        option_type = "CE" if want_call else "PE"

        best = None
        try:
            best = self.selector(strikes=strikes, spot=spot, option_type=option_type)
        except TypeError:
            # some selector signatures differ; try fallback simple call
            try:
                best = self.selector(strikes, spot, option_type)
            except Exception:
                best = None

        if not best:
            logger.warning("No candidate found for %s; skipping", symbol)
            return

        entry_price = float(best.get("premium", 0.0))
        trade = self.book.open_trade(
            symbol=symbol,
            strike=best["strike"],
            option_type=best["option_type"],
            quantity=1.0,
            entry_price=entry_price,
            fees=0.1,
            meta={"selector": "sim"}
        )

        # simulate a single tick move and close
        move_pct = random.uniform(-0.25, 0.25)
        new_premium = round(entry_price * (1 + move_pct), 4)
        self.book.update_mark(trade["id"], new_premium)
        logger.info("Updated mark for trade %s: %.2f (move %+0.2f%%)", trade["id"], new_premium, move_pct * 100)

        closed = self.book.close_trade(trade["id"], exit_price=new_premium)
        logger.info("Closed trade %s realized=%.2f net=%.2f", closed["id"], closed["realized_pnl"], closed["net_pnl"])

    def run(self):
        symbols = self.cfg.get("symbols", ["SYNTH1"])
        for s in symbols:
            try:
                self.run_for_symbol(s)
            except Exception as e:
                logger.exception("Error running symbol %s: %s", s, e)
        logger.info("Simulation summary: %s", self.book.summary())


def load_config(path: str) -> Dict:
    if not YAML_AVAILABLE:
        return {}
    with open(path, "r") as fh:
        return yaml.safe_load(fh)


def setup_logging(level=logging.INFO):
    fmt = "%(asctime)s %(levelname)7s %(name)s - %(message)s"
    logging.basicConfig(level=level, format=fmt)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Simple offline options simulator (no external files required)")
    parser.add_argument("-c", "--config", default=None, help="Optional YAML config path")
    parser.add_argument("--log", default="INFO", help="Log level")
    args = parser.parse_args(argv)

    level = getattr(logging, args.log.upper(), logging.INFO)
    setup_logging(level=level)

    cfg = {}
    if args.config and YAML_AVAILABLE:
        cfg = load_config(args.config)
    else:
        # sensible defaults
        cfg = {
            "symbols": ["NIFTY_SYNTH", "RELIANCE_SYNTH"],
            "seed": 42,
            "selectors": {"delta_range": [0.30, 0.70], "min_open_interest": 10, "min_volume": 0},
            "direction": "random",
        }

    sim = SimpleSim(cfg)
    sim.run()


if __name__ == "__main__":
    main()
