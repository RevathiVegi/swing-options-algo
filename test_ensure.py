from run_sim import ensure_trade_pnl

cases = [
    ({}, 0.0),
    ({'pnl_rupees': ''}, 0.0),
    ({'pnl_rupees': None}, 0.0),
    ({'pnl_rupees': '12.5'}, 12.5),
    ({'pnl_rupees': 7}, 7.0),
    ({'pnl_rupees': 'bad'}, 0.0),
]

def test_ensure_trade_pnl_cases():
    for inp, expected in cases:
        got = ensure_trade_pnl(dict(inp))
        assert float(got['pnl_rupees']) == expected
