import streamlit as st
bash

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QCS // QUANT CONTROL SYSTEM",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  — monochrome dark terminal
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', 'Courier New', monospace !important;
    background-color: #050505 !important;
    color: #d4d4d4 !important;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background-color: #050505 !important; }

.main .block-container {
    background-color: #050505 !important;
    padding: 1.2rem 1.4rem 4rem !important;
    max-width: 1080px !important;
}

#MainMenu,
header[data-testid="stHeader"],
footer,
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] { display: none !important; }

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #111 !important;
    gap: 0 !important;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: .62rem !important;
    font-weight: 600 !important;
    letter-spacing: .18em !important;
    color: #282828 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: .48rem .8rem !important;
    text-transform: uppercase !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #c4c4c4 !important;
    border-bottom: 2px solid #c4c4c4 !important;
    background: transparent !important;
}
[data-testid="stTabs"] button[role="tab"]:hover { color: #666 !important; }

/* ── WIDGETS ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background-color: #0b0b0b !important;
    border: 1px solid #1c1c1c !important;
    border-radius: 1px !important;
    color: #d4d4d4 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: .82rem !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #383838 !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stSelectbox"] > div > div {
    background-color: #0b0b0b !important;
    border: 1px solid #1c1c1c !important;
    border-radius: 1px !important;
    color: #d4d4d4 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: .8rem !important;
}
textarea {
    background-color: #080808 !important;
    border: 1px solid #181818 !important;
    border-radius: 1px !important;
    color: #4a4a4a !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: .72rem !important;
}

/* ── LABELS ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.st-emotion-cache-1kyxreq {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: .58rem !important;
    letter-spacing: .14em !important;
    color: #333 !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] button {
    background: #0b0b0b !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 1px !important;
    color: #666 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: .6rem !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    padding: .38rem 1.1rem !important;
}
[data-testid="stButton"] button:hover {
    border-color: #444 !important;
    color: #d4d4d4 !important;
}

/* ── SLIDER ── */
[data-baseweb="slider"] [role="slider"] {
    background-color: #d4d4d4 !important;
    border-color: #d4d4d4 !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[class*="Track"] {
    background: #1a1a1a !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[class*="Thumb"] {
    background: #d4d4d4 !important;
}

/* ── RADIO & CHECKBOX ── */
[data-testid="stRadio"] label > div > p,
[data-testid="stCheckbox"] label > div > p {
    font-size: .7rem !important;
    color: #555 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── COLUMNS & MISC ── */
[data-testid="column"] { padding: 0 .3rem !important; }
hr { border: none; border-top: 1px solid #0e0e0e; margin: .8rem 0; }
p { margin: 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def get_tier(na: float):
    if na >= 1_000_000:
        return 1, "INSTITUTIONAL MASTER", None, 100.0
    elif na >= 100_000:
        return 2, "PROFESSIONAL TRADER", 1_000_000, min((na - 100_000) / 900_000 * 100, 100.0)
    elif na >= 10_000:
        return 3, "RETAIL OPERATOR", 100_000, min((na - 10_000) / 90_000 * 100, 100.0)
    else:
        return 4, "SEED BUILDER", 10_000, min(na / 10_000 * 100, 100.0)

_REC = {
    ("low_vol_sideways",  "conservative"): 2,
    ("low_vol_sideways",  "aggressive"):   5,
    ("high_vol_bear",     "conservative"): 1,
    ("high_vol_bear",     "aggressive"):   2,
    ("strong_trend_bull", "conservative"): 3,
    ("strong_trend_bull", "aggressive"):  10,
}

def get_rec_lev(regime: str, mode: str) -> int:
    return _REC.get((regime, mode), 2)

def calc_rr(entry: float, target: float, stop: float, direction: str):
    if entry <= 0:
        return 0.0, 0.0, 0.0
    if direction == "LONG":
        up = (target - entry) / entry * 100
        dn = (entry - stop) / entry * 100
    else:
        up = (entry - target) / entry * 100
        dn = (stop - entry) / entry * 100
    rr = up / dn if dn > 0 else 0.0
    return up, dn, rr

def liq_px(entry: float, lev: float, direction: str, mm: float = 0.005) -> float:
    if lev <= 0 or entry <= 0:
        return 0.0
    if direction == "LONG":
        return entry * (1.0 - 1.0 / lev + mm)
    return entry * (1.0 + 1.0 / lev - mm)

def pbar(pct: float, warn: bool = False, h: int = 4) -> str:
    c = "#a81010" if warn else "#d4d4d4"
    p = max(0.0, min(float(pct), 100.0))
    return (
        f'<div style="background:#0c0c0c;height:{h}px;width:100%;margin:.32rem 0">'
        f'<div style="background:{c};height:{h}px;width:{p:.1f}%"></div></div>'
    )

def mbox(lbl: str, val: str, sub: str = "", col: str = "#d4d4d4") -> str:
    sub_html = f'<div style="font-size:.6rem;color:#252525;margin-top:.12rem">{sub}</div>' if sub else ""
    return (
        f'<div style="background:#070707;border:1px solid #131313;'
        f'padding:.68rem .85rem;margin-bottom:.32rem">'
        f'<div style="font-size:.54rem;letter-spacing:.18em;color:#282828;'
        f'text-transform:uppercase;margin-bottom:.18rem">{lbl}</div>'
        f'<div style="font-size:1.25rem;font-weight:600;color:{col};line-height:1.1">{val}</div>'
        f'{sub_html}</div>'
    )

def alert(msg: str, kind: str = "warn") -> str:
    styles = {
        "warn": ("background:#110000;border:1px solid #2c0000;border-left:3px solid #991111;color:#dd3333"),
        "ok":   ("background:#001008;border:1px solid #002416;border-left:3px solid #008830;color:#22aa55"),
        "info": ("background:#060b14;border:1px solid #0c1828;border-left:3px solid #1a3d88;color:#3d6aaa"),
    }
    sty = styles.get(kind, styles["warn"])
    return (
        f'<div style="{sty};padding:.48rem .85rem;margin:.4rem 0;'
        f'font-size:.68rem;letter-spacing:.04em">{msg}</div>'
    )

def sec(lbl: str) -> str:
    return (
        f'<div style="font-size:.53rem;letter-spacing:.22em;color:#222;text-transform:uppercase;'
        f'border-bottom:1px solid #0e0e0e;padding-bottom:.26rem;margin:1.25rem 0 .75rem">{lbl}</div>'
    )

def row(k: str, v: str, vc: str = "#c0c0c0") -> str:
    return (
        f'<div style="display:flex;justify-content:space-between;border-bottom:1px solid #0c0c0c;'
        f'padding:.26rem 0;font-size:.72rem">'
        f'<span style="color:#303030">{k}</span>'
        f'<span style="color:{vc};font-weight:500">{v}</span></div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    # Layer 1
    "ticker": "BTCUSDT",
    "price": 65000.0,
    "vol_phase_idx": 0,       # 0=SURGE 1=AVERAGE 2=CLIFF
    "direction_idx": 0,        # 0=LONG 1=SHORT
    "momentum": 55,
    "ma20": True, "ma50": True, "ma100": False, "ma200": False,
    "support": 62000.0,
    "resistance": 68500.0,
    # Layer 2
    "scenario_idx": 0,         # 0=A 1=B 2=C
    "entry": 65000.0,
    "target": 70000.0,
    "sl": 63000.0,
    "feedback_idx": 0,         # PENDING / TARGET HIT / STOP HIT / TIME CUT / MANUAL EXIT
    "notes": "",
    # Layer 3
    "net_assets": 10000.0,
    "cur_lev": 3.0,
    "regime_idx": 2,           # 0=low_vol 1=high_vol_bear 2=strong_trend_bull
    "risk_mode_idx": 0,        # 0=conservative 1=aggressive
    "rpt": 1.0,
    # Layer 4
    "wins": 7,
    "losses": 3,
    "total_pnl": 1200.0,
    "avg_win": 350.0,
    "avg_loss": 100.0,
    "impulsive": 1,
    "peak": 11500.0,
    "trade_log": [],
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="border-bottom:1px solid #0e0e0e;padding-bottom:.7rem;margin-bottom:1rem">'
    '<div style="font-size:.5rem;letter-spacing:.32em;color:#1e1e1e;text-transform:uppercase;margin-bottom:.12rem">'
    'QUANT CONTROL SYSTEM &nbsp;&middot;&nbsp; v3.0 &nbsp;&middot;&nbsp; ACTIVE SESSION'
    '</div>'
    '<div style="font-size:1.45rem;font-weight:700;color:#b0b0b0;letter-spacing:.04em;line-height:1">'
    'ASSET COMMAND TERMINAL'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
_TABS = st.tabs(["01  TRADE ENGINE", "02  EXPECTATION", "03  CAPITAL OPS", "04  METRICS"])
tab1, tab2, tab3, tab4 = _TABS


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — TRADE ENGINE
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    # ── Cross-layer context bar ───────────────────────────────────────────────
    _na = st.session_state.net_assets
    _tn, _tname, _, _ = get_tier(_na)
    _regime_keys = ["low_vol_sideways", "high_vol_bear", "strong_trend_bull"]
    _regime_cur = _regime_keys[st.session_state.regime_idx]
    _mode_keys = ["conservative", "aggressive"]
    _mode_cur = _mode_keys[st.session_state.risk_mode_idx]
    _rl = get_rec_lev(_regime_cur, _mode_cur)
    st.markdown(
        alert(
            f"CAPITAL CONTEXT &nbsp;&middot;&nbsp; TIER {_tn} [{_tname}]"
            f" &nbsp;|&nbsp; NET ASSETS ${_na:,.0f}"
            f" &nbsp;|&nbsp; REC. LEVERAGE {_rl}x"
            f" &nbsp;|&nbsp; MODE {_mode_cur.upper()}",
            "info",
        ),
        unsafe_allow_html=True,
    )

    # ── Market Identification ─────────────────────────────────────────────────
    st.markdown(sec("MARKET IDENTIFICATION"), unsafe_allow_html=True)
    _vp_opts = ["SURGE", "AVERAGE", "CLIFF"]
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        ticker_val = st.text_input(
            "TICKER",
            value=st.session_state.ticker,
            key="_ticker_widget",
        )
        st.session_state.ticker = ticker_val
    with c2:
        price_val = st.number_input(
            "CURRENT PRICE",
            value=float(st.session_state.price),
            min_value=0.0,
            format="%.4f",
            key="_price_widget",
        )
        st.session_state.price = price_val
    with c3:
        vp_idx = st.selectbox(
            "VOLUME PHASE",
            _vp_opts,
            index=st.session_state.vol_phase_idx,
            key="_vp_widget",
        )
        st.session_state.vol_phase_idx = _vp_opts.index(vp_idx)

    # ── Energy & Direction ────────────────────────────────────────────────────
    st.markdown(sec("ENERGY & DIRECTION SCORING"), unsafe_allow_html=True)
    _dir_opts = ["LONG", "SHORT"]
    c1, c2 = st.columns([1, 2])
    with c1:
        dir_sel = st.radio(
            "DIRECTION",
            _dir_opts,
            index=st.session_state.direction_idx,
            horizontal=True,
            key="_dir_widget",
        )
        st.session_state.direction_idx = _dir_opts.index(dir_sel)
    with c2:
        mom_val = st.slider(
            "MOMENTUM SCORE",
            1, 100,
            value=int(st.session_state.momentum),
            key="_mom_widget",
        )
        st.session_state.momentum = mom_val

    _mc = "#008830" if mom_val >= 60 else ("#991111" if mom_val <= 30 else "#555")
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.65rem;margin:.15rem 0 .6rem">'
        f'<div style="background:#0c0c0c;height:5px;flex:1">'
        f'<div style="background:{_mc};height:5px;width:{mom_val}%"></div></div>'
        f'<span style="font-size:.7rem;color:{_mc};font-weight:600;min-width:3ch">{mom_val}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── MA Matrix ─────────────────────────────────────────────────────────────
    st.markdown(sec("MOVING AVERAGE ALIGNMENT MATRIX"), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ma20_v = st.checkbox("MA 20",  value=st.session_state.ma20,  key="_ma20")
        st.session_state.ma20 = ma20_v
    with c2:
        ma50_v = st.checkbox("MA 50",  value=st.session_state.ma50,  key="_ma50")
        st.session_state.ma50 = ma50_v
    with c3:
        ma100_v = st.checkbox("MA 100", value=st.session_state.ma100, key="_ma100")
        st.session_state.ma100 = ma100_v
    with c4:
        ma200_v = st.checkbox("MA 200", value=st.session_state.ma200, key="_ma200")
        st.session_state.ma200 = ma200_v

    _mas = [("MA20", ma20_v), ("MA50", ma50_v), ("MA100", ma100_v), ("MA200", ma200_v)]
    _ac  = sum(v for _, v in _mas)
    _as  = _ac / 4 * 100
    _mah = '<div style="display:flex;gap:.3rem;flex-wrap:wrap;margin:.2rem 0">'
    for _lbl, _ok in _mas:
        _bg = "#001208" if _ok else "#0a0a0a"
        _fc = "#008830" if _ok else "#242424"
        _bc = "#002414" if _ok else "#111"
        _st = "ALIGNED" if _ok else "-- OFF"
        _mah += (
            f'<div style="background:{_bg};border:1px solid {_bc};padding:.3rem .65rem">'
            f'<div style="font-size:.52rem;color:#222;margin-bottom:.06rem">{_lbl}</div>'
            f'<div style="font-size:.62rem;color:{_fc}">{_st}</div></div>'
        )
    _mah += (
        f'</div>'
        f'<div style="font-size:.56rem;color:#222;margin-top:.22rem">'
        f'ALIGNMENT {_ac}/4 &nbsp;&middot;&nbsp; {_as:.0f}%</div>'
    )
    st.markdown(_mah, unsafe_allow_html=True)

    # ── Key Price Levels ──────────────────────────────────────────────────────
    st.markdown(sec("KEY PRICE LEVELS"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        sup_val = st.number_input(
            "SUPPORT LEVEL",
            value=float(st.session_state.support),
            min_value=0.0,
            format="%.4f",
            key="_sup_widget",
        )
        st.session_state.support = sup_val
    with c2:
        res_val = st.number_input(
            "RESISTANCE LEVEL",
            value=float(st.session_state.resistance),
            min_value=0.0,
            format="%.4f",
            key="_res_widget",
        )
        st.session_state.resistance = res_val

    _p, _s, _r = price_val, sup_val, res_val
    if _r > _s > 0 and _p > 0:
        _pp = max(0.0, min((_p - _s) / (_r - _s) * 100, 100.0))
        _dr = (_r - _p) / _p * 100
        _ds = (_p - _s) / _p * 100
        st.markdown(
            f'<div style="margin:.45rem 0">'
            f'<div style="display:flex;justify-content:space-between;font-size:.55rem;color:#252525;margin-bottom:.22rem">'
            f'<span>SUP &nbsp;{_s:,.2f}</span><span>RES &nbsp;{_r:,.2f}</span></div>'
            f'<div style="background:#0c0c0c;height:7px;width:100%;position:relative">'
            f'<div style="position:absolute;top:0;left:{_pp:.1f}%;width:2px;height:7px;'
            f'background:#c0c0c0;transform:translateX(-50%)"></div></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:.55rem;color:#2e2e2e;margin-top:.22rem">'
            f'<span>+{_ds:.2f}% above support</span><span>{_dr:.2f}% to resistance</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Signal Synthesis ──────────────────────────────────────────────────────
    st.markdown(sec("COMPOSITE SIGNAL SYNTHESIS"), unsafe_allow_html=True)
    _dir = _dir_opts[st.session_state.direction_idx]
    _vp  = _vp_opts[st.session_state.vol_phase_idx]
    _sig = 0
    if _dir == "LONG":
        _sig += 25 if _vp == "SURGE" else (10 if _vp == "AVERAGE" else 0)
    else:
        _sig += 25 if _vp == "CLIFF" else (10 if _vp == "AVERAGE" else 0)
    _sig += int(mom_val * 0.4)
    _sig += int(_as * 0.35)
    _sig = min(_sig, 100)
    _sc  = "#009933" if _sig >= 65 else ("#aa7700" if _sig >= 40 else "#991111")
    _sl  = "STRONG SIGNAL" if _sig >= 65 else ("MODERATE SIGNAL" if _sig >= 40 else "WEAK SIGNAL")
    _dc  = "#009933" if _dir == "LONG" else "#991111"
    st.markdown(
        f'<div style="background:#070707;border:1px solid #111;padding:.85rem 1rem">'
        f'<div style="display:flex;justify-content:space-between;align-items:center">'
        f'<div>'
        f'<div style="font-size:.53rem;letter-spacing:.18em;color:#1e1e1e;text-transform:uppercase">COMPOSITE SIGNAL</div>'
        f'<div style="font-size:1.65rem;font-weight:700;color:{_sc};line-height:1.1">'
        f'{_sig}<span style="font-size:.82rem;font-weight:400;color:#242424">/100</span></div>'
        f'</div>'
        f'<div style="text-align:right">'
        f'<div style="font-size:.6rem;color:{_sc};letter-spacing:.1em">{_sl}</div>'
        f'<div style="font-size:.7rem;color:{_dc};font-weight:600;margin-top:.12rem">{_dir}</div>'
        f'</div></div>'
        f'<div style="background:#0c0c0c;height:3px;margin-top:.6rem">'
        f'<div style="background:{_sc};height:3px;width:{_sig}%"></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — EXPECTATION ENGINE
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    _scen_opts  = ["A — MAIN SCENARIO", "B — TREND REVERSAL", "C — BLACK SWAN"]
    _scen_descs = [
        "Primary thesis intact. Execute at full conviction. Trend continues per plan.",
        "Trend invalidated. Scale down. Hedge or reverse position. Reassess structure.",
        "Extreme tail-risk event. Suspend all positions. Capital preservation mode only.",
    ]
    _fb_opts = ["PENDING", "TARGET HIT", "STOP HIT", "TIME CUT", "MANUAL EXIT"]

    st.markdown(sec("SCENARIO SELECTION"), unsafe_allow_html=True)
    scen_sel = st.radio(
        "ACTIVE SCENARIO",
        _scen_opts,
        index=st.session_state.scenario_idx,
        horizontal=True,
        key="_scen_widget",
    )
    st.session_state.scenario_idx = _scen_opts.index(scen_sel)
    _si = st.session_state.scenario_idx
    st.markdown(
        f'<div style="font-size:.7rem;color:#3a3a3a;margin:.28rem 0 .7rem;font-style:italic">'
        f'{_scen_descs[_si]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(sec("ENTRY POINT CALCULATOR"), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        entry_val = st.number_input(
            "ENTRY PRICE",
            value=float(st.session_state.entry),
            min_value=0.0,
            format="%.4f",
            key="_entry_widget",
        )
        st.session_state.entry = entry_val
    with c2:
        target_val = st.number_input(
            "TARGET (TAKE PROFIT)",
            value=float(st.session_state.target),
            min_value=0.0,
            format="%.4f",
            key="_target_widget",
        )
        st.session_state.target = target_val
    with c3:
        sl_val = st.number_input(
            "STOP LOSS",
            value=float(st.session_state.sl),
            min_value=0.0,
            format="%.4f",
            key="_sl_widget",
        )
        st.session_state.sl = sl_val

    _dir2 = _dir_opts[st.session_state.direction_idx]
    _up, _dn, _rr = calc_rr(entry_val, target_val, sl_val, _dir2)

    st.markdown(sec("RISK / REWARD VERIFICATION"), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(mbox("UPSIDE",   f"+{_up:.2f}%", "to target",   "#009933"), unsafe_allow_html=True)
    c2.markdown(mbox("DOWNSIDE", f"-{_dn:.2f}%", "to stop loss","#991111"), unsafe_allow_html=True)
    _rrv = "#d4d4d4" if _rr >= 2.0 else "#991111"
    c3.markdown(mbox("R:R RATIO", f"1 : {_rr:.2f}", "risk-reward", _rrv), unsafe_allow_html=True)
    _rr_bar = min(_rr / 4 * 100, 100)
    c4.markdown(
        f'<div style="background:#070707;border:1px solid #111;padding:.68rem .85rem">'
        f'<div style="font-size:.54rem;letter-spacing:.18em;color:#282828;'
        f'text-transform:uppercase;margin-bottom:.45rem">RR GAUGE</div>'
        f'{pbar(_rr_bar, warn=_rr < 2.0, h=5)}'
        f'<div style="font-size:.58rem;color:#252525;margin-top:.28rem">'
        f'{"VALID" if _rr >= 2.0 else "BELOW MIN"} &middot; MIN 1:2</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if _rr < 2.0:
        st.markdown(
            alert(
                f"RISK/REWARD BELOW THRESHOLD &nbsp;&middot;&nbsp; Current {_rr:.2f} "
                f"&nbsp;&middot;&nbsp; Minimum required 2.00 "
                f"&nbsp;&middot;&nbsp; Adjust entry, target, or stop loss before proceeding.",
                "warn",
            ),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            alert(
                f"RISK/REWARD VALIDATED &nbsp;&middot;&nbsp; {_rr:.2f}:1 "
                f"&nbsp;&middot;&nbsp; Trade structure meets minimum criteria.",
                "ok",
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        row("Direction", _dir2)
        + row("Entry  →  Target", f"{entry_val:,.4f} &nbsp;→&nbsp; {target_val:,.4f}")
        + row("Entry  →  Stop",   f"{entry_val:,.4f} &nbsp;→&nbsp; {sl_val:,.4f}")
        + row("Profit distance",  f"{'+'}{abs(target_val - entry_val):,.4f}")
        + row("Loss distance",    f"-{abs(entry_val - sl_val):,.4f}"),
        unsafe_allow_html=True,
    )

    st.markdown(sec("POST-TRADE FEEDBACK LOOP"), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        fb_sel = st.selectbox(
            "TRADE OUTCOME",
            _fb_opts,
            index=st.session_state.feedback_idx,
            key="_fb_widget",
        )
        st.session_state.feedback_idx = _fb_opts.index(fb_sel)
    with c2:
        notes_val = st.text_area(
            "TRADE NOTES / DEBRIEF",
            value=st.session_state.notes,
            height=78,
            placeholder="Post-trade analysis, market behavior vs expectation...",
            key="_notes_widget",
        )
        st.session_state.notes = notes_val

    _fb_cols = {
        "PENDING":     "#333",
        "TARGET HIT":  "#009933",
        "STOP HIT":    "#991111",
        "TIME CUT":    "#666",
        "MANUAL EXIT": "#886600",
    }
    _fc = _fb_cols.get(fb_sel, "#333")
    st.markdown(
        f'<div style="border-left:3px solid {_fc};padding:.38rem .8rem;'
        f'font-size:.68rem;color:{_fc};margin-top:.4rem;background:#08080a">'
        f'STATUS: {fb_sel} &nbsp;&middot;&nbsp; SCENARIO: {scen_sel[0]}</div>',
        unsafe_allow_html=True,
    )

    if st.button("LOG TRADE TO HISTORY", key="_log_btn"):
        _rpt_pct = st.session_state.rpt
        _na_cur  = st.session_state.net_assets
        _risk_amt = _na_cur * _rpt_pct / 100
        _trade_rec = {
            "ticker":    st.session_state.ticker,
            "direction": _dir2,
            "entry":     entry_val,
            "target":    target_val,
            "stop":      sl_val,
            "rr":        _rr,
            "scenario":  scen_sel[0],
            "outcome":   fb_sel,
            "notes":     notes_val,
        }
        st.session_state.trade_log.append(_trade_rec)
        if fb_sel == "TARGET HIT":
            st.session_state.wins += 1
            _pnl = _risk_amt * _rr
            st.session_state.total_pnl  += _pnl
            st.session_state.net_assets  = _na_cur + _pnl
            if st.session_state.net_assets > st.session_state.peak:
                st.session_state.peak = st.session_state.net_assets
        elif fb_sel == "STOP HIT":
            st.session_state.losses     += 1
            st.session_state.total_pnl  -= _risk_amt
            st.session_state.net_assets  = _na_cur - _risk_amt
        st.markdown(alert("Trade logged to session history.", "ok"), unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — CAPITAL OPERATION
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    _regime_disp = [
        "LOW VOL — SIDEWAYS",
        "HIGH VOL — BEAR",
        "STRONG TREND — BULL",
    ]
    _mode_disp = ["CONSERVATIVE", "AGGRESSIVE"]

    st.markdown(sec("CAPITAL CONTROL"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        na_val = st.number_input(
            "NET ASSETS  ($)",
            value=float(st.session_state.net_assets),
            min_value=0.0,
            format="%.2f",
            key="_na_widget",
        )
        st.session_state.net_assets = na_val
    with c2:
        cl_val = st.number_input(
            "CURRENT LEVERAGE  (x)",
            value=float(st.session_state.cur_lev),
            min_value=0.0,
            max_value=125.0,
            step=0.5,
            format="%.1f",
            key="_cl_widget",
        )
        st.session_state.cur_lev = cl_val

    st.markdown(sec("MARKET REGIME & RISK MODE"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        reg_sel = st.selectbox(
            "MARKET REGIME",
            _regime_disp,
            index=st.session_state.regime_idx,
            key="_reg_widget",
        )
        st.session_state.regime_idx = _regime_disp.index(reg_sel)
    with c2:
        mode_sel = st.selectbox(
            "RISK MODE",
            _mode_disp,
            index=st.session_state.risk_mode_idx,
            key="_mode_widget",
        )
        st.session_state.risk_mode_idx = _mode_disp.index(mode_sel)

    _regime_cur3 = _regime_keys[st.session_state.regime_idx]
    _mode_cur3   = _mode_keys[st.session_state.risk_mode_idx]
    _rl3         = get_rec_lev(_regime_cur3, _mode_cur3)
    _lv_var      = cl_val - _rl3
    _lv_warn     = _lv_var > 0
    _util        = (cl_val / _rl3 * 100) if _rl3 > 0 else 100.0
    _free_m      = na_val * (_rl3 - cl_val) / _rl3 if _rl3 > 0 else 0.0

    st.markdown(sec("LEVERAGE ANALYSIS"), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(mbox("CURRENT LEV",  f"{cl_val:.1f}x", "active leverage"), unsafe_allow_html=True)
    c2.markdown(mbox("RECOMMENDED",  f"{_rl3}x", f"{reg_sel[:14]}..."), unsafe_allow_html=True)
    _vc3 = "#991111" if _lv_warn else "#009933"
    _vs3 = f"{'+'}{_lv_var:.1f}x" if _lv_var >= 0 else f"{_lv_var:.1f}x"
    c3.markdown(mbox("VARIANCE", _vs3, "vs recommended", _vc3), unsafe_allow_html=True)
    _fm = max(_free_m, 0.0)
    c4.markdown(mbox("FREE MARGIN", f"${_fm:,.0f}", f"{max(100 - _util, 0):.0f}% remaining",
                     "#991111" if _lv_warn else "#d4d4d4"), unsafe_allow_html=True)

    if _lv_warn:
        st.markdown(
            alert(
                f"LEVERAGE EXCEEDS RECOMMENDED &nbsp;&middot;&nbsp; "
                f"Current {cl_val:.1f}x vs Recommended {_rl3}x &nbsp;&middot;&nbsp; "
                f"+{_lv_var:.1f}x over limit &nbsp;&middot;&nbsp; Reduce exposure immediately.",
                "warn",
            ),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            alert(
                f"LEVERAGE WITHIN BOUNDS &nbsp;&middot;&nbsp; "
                f"{cl_val:.1f}x of {_rl3}x recommended &nbsp;&middot;&nbsp; "
                f"${_fm:,.0f} headroom available.",
                "ok",
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="font-size:.52rem;letter-spacing:.15em;color:#222;text-transform:uppercase;margin-bottom:.28rem">LEVERAGE UTILIZATION &nbsp;{_util:.0f}%</div>'
        + pbar(min(_util, 100), warn=_util > 100, h=5),
        unsafe_allow_html=True,
    )

    # ── Capital Tier ──────────────────────────────────────────────────────────
    st.markdown(sec("CAPITAL TIER STATUS"), unsafe_allow_html=True)
    _tn3, _tname3, _tnext3, _tpct3 = get_tier(na_val)
    _tier_colors = {1: "#c8a020", 2: "#5588bb", 3: "#888888", 4: "#444"}
    _tc3 = _tier_colors.get(_tn3, "#444")
    _next_str = (
        f'<div style="font-size:.62rem;color:#252525">'
        f'Next: TIER {_tn3 - 1} &nbsp;@ &nbsp;${_tnext3:,.0f}</div>'
        if _tnext3 else
        '<div style="font-size:.62rem;color:#555">APEX TIER ACHIEVED</div>'
    )
    _prog_blk = (
        f'<div style="margin-top:.75rem">'
        f'<div style="display:flex;justify-content:space-between;font-size:.56rem;color:#1e1e1e;margin-bottom:.22rem">'
        f'<span>TIER {_tn3} PROGRESS</span><span>{_tpct3:.1f}%</span></div>'
        f'<div style="background:#0c0c0c;height:4px">'
        f'<div style="background:{_tc3};height:4px;width:{_tpct3:.1f}%"></div></div>'
        f'<div style="font-size:.56rem;color:#1e1e1e;margin-top:.22rem">'
        f'${_tnext3 - na_val:,.0f} to TIER {_tn3 - 1}</div></div>'
        if _tnext3 else
        f'<div style="margin-top:.55rem;font-size:.62rem;color:#555">Maximum capital tier achieved.</div>'
    )
    st.markdown(
        f'<div style="background:#070707;border:1px solid #111;padding:.95rem 1rem">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'<div>'
        f'<div style="font-size:.52rem;letter-spacing:.2em;color:#1e1e1e;margin-bottom:.18rem">CURRENT TIER</div>'
        f'<div style="font-size:1.25rem;font-weight:700;color:{_tc3}">TIER {_tn3}</div>'
        f'<div style="font-size:.7rem;color:#444;letter-spacing:.08em">{_tname3}</div>'
        f'</div>'
        f'<div style="text-align:right">'
        f'<div style="font-size:.52rem;letter-spacing:.15em;color:#1e1e1e;margin-bottom:.18rem">NET ASSETS</div>'
        f'<div style="font-size:1.25rem;font-weight:600;color:#c0c0c0">${na_val:,.0f}</div>'
        f'{_next_str}'
        f'</div></div>'
        f'{_prog_blk}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Position Sizing (integrates Layer 2) ──────────────────────────────────
    st.markdown(sec("OPTIMAL POSITION SIZING  ·  INTEGRATED FROM LAYER 2"), unsafe_allow_html=True)

    _dir3 = _dir_opts[st.session_state.direction_idx]
    _up3, _dn3, _rr3 = calc_rr(
        st.session_state.entry,
        st.session_state.target,
        st.session_state.sl,
        _dir3,
    )

    c1, c2 = st.columns(2)
    with c1:
        rpt_val = st.number_input(
            "RISK PER TRADE  (% of capital)",
            value=float(st.session_state.rpt),
            min_value=0.01,
            max_value=20.0,
            step=0.1,
            format="%.2f",
            key="_rpt_widget",
        )
        st.session_state.rpt = rpt_val
    with c2:
        st.markdown(
            f'<div style="background:#070707;border:1px solid #111;padding:.68rem .85rem;margin-top:.28rem">'
            f'<div style="font-size:.54rem;letter-spacing:.18em;color:#282828;text-transform:uppercase;margin-bottom:.18rem">SL FROM LAYER 2</div>'
            f'<div style="font-size:1.1rem;font-weight:600;color:#991111">-{_dn3:.2f}%</div>'
            f'<div style="font-size:.58rem;color:#252525;margin-top:.1rem">'
            f'{st.session_state.entry:,.4f} &nbsp;&rarr;&nbsp; {st.session_state.sl:,.4f}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    _risk_usd = na_val * rpt_val / 100
    if _dn3 > 0:
        _pos_notional = _risk_usd / (_dn3 / 100)
    else:
        _pos_notional = 0.0
    _margin_req = _pos_notional / cl_val if cl_val > 0 else 0.0

    c1, c2, c3 = st.columns(3)
    c1.markdown(mbox("RISK AMOUNT",   f"${_risk_usd:,.2f}",   f"{rpt_val:.2f}% of capital"), unsafe_allow_html=True)
    c2.markdown(mbox("POSITION SIZE", f"${_pos_notional:,.0f}", "notional value"), unsafe_allow_html=True)
    c3.markdown(mbox("MARGIN REQ.",   f"${_margin_req:,.0f}",  f"at {cl_val:.1f}x leverage"), unsafe_allow_html=True)

    # ── Liquidation Check ─────────────────────────────────────────────────────
    _liq = liq_px(st.session_state.entry, cl_val, _dir3)
    _sl3 = st.session_state.sl

    if _dir3 == "LONG":
        _liq_danger = (_liq > _sl3) and (_liq > 0) and (_sl3 > 0)
    else:
        _liq_danger = (_liq < _sl3) and (_liq > 0) and (_sl3 > 0)

    _liq_col = "#991111" if _liq_danger else "#d4d4d4"
    _liq_txt = "!! LIQ BEFORE STOP LOSS" if _liq_danger else "SAFE — STOP TRIGGERS FIRST"
    st.markdown(
        f'<div style="background:{"#100000" if _liq_danger else "#070707"};'
        f'border:1px solid {"#280000" if _liq_danger else "#111"};'
        f'{"border-left:3px solid #880000;" if _liq_danger else ""}'
        f'padding:.8rem 1rem;margin:.45rem 0">'
        f'<div style="display:flex;justify-content:space-between;align-items:center">'
        f'<div>'
        f'<div style="font-size:.54rem;letter-spacing:.17em;color:#282828;text-transform:uppercase;margin-bottom:.18rem">'
        f'ISOLATED MARGIN LIQUIDATION PRICE</div>'
        f'<div style="font-size:1.35rem;font-weight:700;color:{_liq_col}">{_liq:,.4f}</div>'
        f'</div>'
        f'<div style="text-align:right">'
        f'<div style="font-size:.6rem;color:{_liq_col};letter-spacing:.08em">{_liq_txt}</div>'
        f'<div style="font-size:.6rem;color:#252525;margin-top:.18rem">STOP LOSS: {_sl3:,.4f}</div>'
        f'</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if _liq_danger:
        st.markdown(
            alert(
                "SYSTEM LOCK — FATAL RISK DETECTED &nbsp;&middot;&nbsp; "
                f"Liquidation {_liq:,.4f} triggers BEFORE stop loss {_sl3:,.4f} "
                f"&nbsp;&middot;&nbsp; Reduce leverage or widen stop. "
                "Trade execution is suspended until resolved.",
                "warn",
            ),
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — METRICS & LOGISTICS
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(sec("PERFORMANCE INPUT"), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        wins_val = st.number_input(
            "WINNING TRADES",
            value=int(st.session_state.wins),
            min_value=0,
            step=1,
            key="_wins_widget",
        )
        st.session_state.wins = wins_val
    with c2:
        losses_val = st.number_input(
            "LOSING TRADES",
            value=int(st.session_state.losses),
            min_value=0,
            step=1,
            key="_losses_widget",
        )
        st.session_state.losses = losses_val
    with c3:
        pnl_val = st.number_input(
            "TOTAL CUMULATIVE PNL  ($)",
            value=float(st.session_state.total_pnl),
            format="%.2f",
            key="_pnl_widget",
        )
        st.session_state.total_pnl = pnl_val

    c1, c2, c3 = st.columns(3)
    with c1:
        _imp_max = max(int(losses_val), 1)
        _imp_cur = min(int(st.session_state.impulsive), int(losses_val))
        imp_val = st.number_input(
            "IMPULSIVE LOSSES (UNDISCIPLINED)",
            value=_imp_cur,
            min_value=0,
            max_value=_imp_max,
            step=1,
            key="_imp_widget",
        )
        st.session_state.impulsive = min(imp_val, losses_val)
    with c2:
        avg_win_val = st.number_input(
            "AVG WIN  ($)",
            value=float(st.session_state.avg_win),
            min_value=0.0,
            format="%.2f",
            key="_avgw_widget",
        )
        st.session_state.avg_win = avg_win_val
    with c3:
        avg_loss_val = st.number_input(
            "AVG LOSS  ($)",
            value=float(st.session_state.avg_loss),
            min_value=0.0,
            format="%.2f",
            key="_avgl_widget",
        )
        st.session_state.avg_loss = avg_loss_val

    c1, c2 = st.columns(2)
    with c1:
        peak_val = st.number_input(
            "PEAK ACCOUNT VALUE  ($)",
            value=float(max(st.session_state.peak, st.session_state.net_assets)),
            min_value=0.0,
            format="%.2f",
            key="_peak_widget",
        )
        st.session_state.peak = peak_val

    # ── Statistical Metrics ────────────────────────────────────────────────────
    _tt   = wins_val + losses_val
    _wr   = wins_val / _tt * 100 if _tt > 0 else 0.0

    if avg_loss_val > 0 and losses_val > 0 and wins_val > 0:
        _pf = (wins_val * avg_win_val) / (losses_val * avg_loss_val)
    else:
        _pf = 0.0

    _mdd   = (peak_val - st.session_state.net_assets) / peak_val * 100 if peak_val > 0 else 0.0
    _mdd   = max(_mdd, 0.0)
    _disc_l = losses_val - min(st.session_state.impulsive, losses_val)
    _disc   = _disc_l / losses_val * 100 if losses_val > 0 else 100.0

    st.markdown(sec("STATISTICAL PERFORMANCE METRICS"), unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    _wrc = "#009933" if _wr >= 50 else "#991111"
    c1.markdown(mbox("WIN RATE",      f"{_wr:.1f}%",      f"{wins_val}W / {losses_val}L", _wrc), unsafe_allow_html=True)
    c2.markdown(mbox("TOTAL TRADES",  f"{_tt}",          f"${pnl_val:+,.2f} net"), unsafe_allow_html=True)
    _pfc = "#009933" if _pf >= 1.5 else ("#aa7700" if _pf >= 1.0 else "#991111")
    c3.markdown(mbox("PROFIT FACTOR", f"{_pf:.2f}",      "gross win/loss ratio", _pfc), unsafe_allow_html=True)
    _mddc = "#991111" if _mdd > 20 else ("#aa7700" if _mdd > 10 else "#d4d4d4")
    c4.markdown(mbox("MAX DRAWDOWN",  f"-{_mdd:.1f}%",   f"Peak ${peak_val:,.0f}", _mddc), unsafe_allow_html=True)

    # ── Edge Analysis ─────────────────────────────────────────────────────────
    st.markdown(sec("MATHEMATICAL EDGE ANALYSIS"), unsafe_allow_html=True)
    _dir4 = _dir_opts[st.session_state.direction_idx]
    _up4, _dn4, _rr4 = calc_rr(
        st.session_state.entry,
        st.session_state.target,
        st.session_state.sl,
        _dir4,
    )
    _ev   = (_wr / 100 * _rr4) - (1 - _wr / 100) if _rr4 > 0 else 0.0
    _bkwr = 1 / (1 + _rr4) * 100 if _rr4 > 0 else 50.0
    _evc  = "#009933" if _ev > 0 else "#991111"
    _wdiff = _wr - _bkwr
    _wdc  = "#009933" if _wdiff >= 0 else "#991111"
    _n30  = f"{max(30 - _tt, 0)} more trades needed" if _tt < 30 else "SUFFICIENT SAMPLE (n>=30)"

    st.markdown(
        row("Current R:R Ratio (Layer 2)", f"1 : {_rr4:.2f}")
        + row("Expected Value per trade (in R)", f"{_ev:+.3f}R", _evc)
        + row("Break-even win rate at current R:R", f"{_bkwr:.1f}%")
        + row("Win rate edge over break-even", f"{_wdiff:+.1f}%", _wdc)
        + row("Statistical significance", _n30),
        unsafe_allow_html=True,
    )

    if _ev > 0:
        st.markdown(
            alert(
                f"POSITIVE EDGE CONFIRMED &nbsp;&middot;&nbsp; EV {_ev:+.3f}R per trade "
                f"&nbsp;&middot;&nbsp; System carries mathematical advantage.",
                "ok",
            ),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            alert(
                f"NEGATIVE EDGE DETECTED &nbsp;&middot;&nbsp; EV {_ev:+.3f}R "
                f"&nbsp;&middot;&nbsp; Improve win rate or tighten R:R ratio.",
                "warn",
            ),
            unsafe_allow_html=True,
        )

    # ── Discipline Tracker ────────────────────────────────────────────────────
    st.markdown(sec("TRADER DISCIPLINE & METACOGNITION"), unsafe_allow_html=True)
    _dsc = "#009933" if _disc >= 80 else ("#aa7700" if _disc >= 60 else "#991111")
    _dsl = "HIGH DISCIPLINE" if _disc >= 80 else ("MODERATE" if _disc >= 60 else "UNDISCIPLINED")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(mbox("DISCIPLINE SCORE", f"{_disc:.0f}%", _dsl, _dsc), unsafe_allow_html=True)
    with c2:
        _imp_cnt = min(int(st.session_state.impulsive), int(losses_val))
        st.markdown(
            f'<div style="background:#070707;border:1px solid #111;padding:.68rem .95rem">'
            f'<div style="font-size:.54rem;letter-spacing:.17em;color:#282828;text-transform:uppercase;margin-bottom:.5rem">LOSS CLASSIFICATION</div>'
            + row("Disciplined &nbsp;(rule-based stop)",   str(_disc_l), "#009933")
            + row("Impulsive &nbsp;(deviation from plan)", str(_imp_cnt), "#991111")
            + row("Discipline ratio",                      f"{_disc:.0f}%", _dsc)
            + f'<div style="background:#0c0c0c;height:4px;margin-top:.55rem">'
            f'<div style="background:{_dsc};height:4px;width:{_disc:.0f}%"></div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if _mdd > 20:
        st.markdown(
            alert(
                f"CRITICAL DRAWDOWN &nbsp;&middot;&nbsp; -{_mdd:.1f}% from peak ${peak_val:,.0f} "
                f"&nbsp;&middot;&nbsp; Reduce risk per trade and reassess strategy immediately.",
                "warn",
            ),
            unsafe_allow_html=True,
        )
    elif _mdd > 10:
        st.markdown(
            alert(
                f"MODERATE DRAWDOWN &nbsp;&middot;&nbsp; -{_mdd:.1f}% &nbsp;&middot;&nbsp; "
                "Monitor closely. Consider reducing position size.",
                "info",
            ),
            unsafe_allow_html=True,
        )

    # ── Trade Log ─────────────────────────────────────────────────────────────
    _log = st.session_state.trade_log
    if _log:
        st.markdown(
            sec(f"TRADE HISTORY &nbsp;&middot;&nbsp; {len(_log)} ENTRIES"),
            unsafe_allow_html=True,
        )
        _oc_colors = {
            "TARGET HIT":  "#009933",
            "STOP HIT":    "#991111",
            "PENDING":     "#333",
            "TIME CUT":    "#555",
            "MANUAL EXIT": "#886600",
        }
        _show = list(reversed(_log[-12:]))
        for _i, _t in enumerate(_show):
            _idx = len(_log) - _i
            _oc  = _t.get("outcome", "PENDING")
            _occ = _oc_colors.get(_oc, "#333")
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'border-bottom:1px solid #0c0c0c;padding:.24rem 0;font-size:.68rem">'
                f'<span style="color:#333">{_idx}.</span>'
                f'<span style="color:#555">{_t.get("ticker","?")}&nbsp;{_t.get("direction","?")}</span>'
                f'<span style="color:#353535">E:{_t.get("entry",0):,.2f}</span>'
                f'<span style="color:#353535">SL:{_t.get("stop",0):,.2f}</span>'
                f'<span style="color:#353535">RR:{_t.get("rr",0):.2f}</span>'
                f'<span style="color:{_occ}">{_oc}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if st.button("CLEAR HISTORY", key="_clear_btn"):
            st.session_state.trade_log = []
            st.rerun()
ENDOFFILE
echo "Done — $(wc -l < /mnt/user-data/outputs/qcs_app.py) lines"
