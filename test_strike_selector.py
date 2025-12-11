from swing_options.strike_selector import select_itm_strike

def make_rec(strike, typ, delta=0.5, oi=100, vol=10, premium=1.0):
    return {
        "strike": strike,
        "option_type": typ,
        "delta": delta,
        "open_interest": oi,
        "volume": vol,
        "premium": premium,
    }

def test_select_itm_nearest():
    strikes = [make_rec(15000,"CE"), make_rec(15100,"CE"), make_rec(14900,"CE")]
    chosen = select_itm_strike(strikes, spot=15050, option_type="CE")
    assert chosen is not None
    assert float(chosen["strike"]) in (15000, 15100)

def test_filters_and_fallback():
    # create a candidate that fails OI filter and one that passes
    s1 = make_rec(15000, "CE", oi=0)   # low OI
    s2 = make_rec(14900, "CE", oi=50)  # ok
    chosen = select_itm_strike([s1, s2], spot=15050, option_type="CE", min_open_interest=10)
    assert chosen is not None
    assert float(chosen["strike"]) == 14900
