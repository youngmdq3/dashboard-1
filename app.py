import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 기본 설정
st.set_page_config(page_title="OWNER TRADING SYSTEM", layout="wide")

# 무채색 오너 감성의 딥 다크 커스텀 스타일
st.markdown("""
    <style>
    .reportview-container, .main { background-color: #0b0b0b; color: #e0e0e0; }
    .sidebar .sidebar-content { background-color: #121212; }
    h1, h2, h3, h4 { color: #ffffff !important; font-family: 'Courier New', monospace; letter-spacing: 1px; }
    .stButton>button { background-color: #222222; color: white; border: 1px solid #444444; }
    .stButton>button:hover { background-color: #333333; border: 1px solid #ffffff; }
    </style>
""", unsafe_allow_html=True)

# 2. 사이드바 구성 (오너 관제 센터)
st.sidebar.title("🦅 OWNER CONTROL CENTER")
st.sidebar.markdown("---")

market_phase = st.sidebar.selectbox(
    "MARKET PHASE (시장 국면)",
    ["선택하세요", "고변동성 하락장 (리스크 극대화)", "저변동성 횡보장", "강한 추세 상승장"]
)

op_mode = st.sidebar.radio("OPERATION MODE (운영 모드)", ["보수형 (Conservative)", "공격형 (Aggressive)"])

st.sidebar.markdown("---")
st.sidebar.markdown("**TRADER DISCIPLINE**")
st.sidebar.caption("계획되지 않은 진입은 자산의 죽음을 의미한다.")

# 3. 메인 화면 - 타이틀
st.title("🎛️ OWNER TRADING SYSTEM")
st.markdown("`단 한 명의 지배자를 위한 독점적 자산 관제탑`")
st.markdown("---")

# 4. [운영 레이어] 자산 및 레버리지 자동 계산 로직
st.subheader("📊 LAYER 1: OPERATION (자산 운용 가이드라인)")

col1, col2, col3 = st.columns(3)
with col1:
    current_seed = st.number_input("현재 총 투자 자산 ($)", value=10000, step=1000)
with col2:
    if market_phase == "고변동성 하락장 (리스크 극대화)":
        recommended_lev = 1.0 if op_mode == "보수형 (Conservative)" else 2.0
    elif market_phase == "강한 추세 상승장":
        recommended_lev = 3.0 if op_mode == "보수형 (Conservative)" else 5.0
    else:
        recommended_lev = 1.5 if op_mode == "보수형 (Conservative)" else 3.0
    
    st.metric(label="📊 국면별 권장 레버리지", value=f"{recommended_lev}x")
with col3:
    max_position = current_seed * recommended_lev
    st.metric(label="🛡️ 최대 허용 포지션 규모", value=f"${max_position:,.0f}")

st.markdown("---")

# 5. [신규 탑재] 실전 포지션 빌더 & 리스크 계산기
st.subheader("⚡ LAYER 2: POSITION BUILDER (실시간 리스크 계산기)")
st.markdown("포지션 진입 전, 손익비와 리스크 한도를 초과하지 않는지 계산합니다.")

calc_col1, calc_col2 = st.columns(2)

with calc_col1:
    st.markdown("##### 📥 Entry Parameters")
    position_side = st.selectbox("포지션 방향", ["LONG", "SHORT"])
    entry_price = st.number_input("진입 가격 (Entry)", value=100.0, step=0.1)
    sl_price = st.number_input("손절 가격 (Stop Loss)", value=95.0, step=0.1)
    tp_price = st.number_input("익절 가격 (Take Profit)", value=115.0, step=0.1)

with calc_col2:
    st.markdown("##### 📊 Risk & Reward Metrics")
    
    # 손익비 및 리스크 계산 로직
    if position_side == "LONG":
        risk_pct = ((entry_price - sl_price) / entry_price) * 100 if entry_price > 0 else 0
        reward_pct = ((tp_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0
    else:
        risk_pct = ((sl_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0
        reward_pct = ((entry_price - tp_price) / entry_price) * 100 if entry_price > 0 else 0
        
    rr_ratio = (reward_pct / risk_pct) if risk_pct > 0 else 0
    
    # 오너가 감당하는 실제 달러 리스크 (최대 포지션 규모 기준 세팅)
    expected_loss = max_position * (risk_pct / 100)
    expected_gain = max_position * (reward_pct / 100)
    
    # 지표 출력
    st.metric(label="🎯 리스크 대비 보상 비율 (손익비)", value=f"1 : {rr_ratio:.2f}")
    st.metric(label="🚨 손절 시 예상 손실 금액", value=f"${expected_loss:,.2f}", delta=f"-{risk_pct:.2f}%", delta_color="inverse")
    st.metric(label="💰 익절 시 예상 수익 금액", value=f"${expected_gain:,.2f}", delta=f"+{reward_pct:.2f}%")

    # 메타인지 통제 장치
    if rr_ratio < 2.0:
        st.warning("⚠️ 손익비가 1:2 미만입니다. 손익비가 좋지 않은 자리는 오너의 진입 대상이 아닙니다.")
    else:
        st.success("✅ 합리적인 손익비 구간입니다. 규율 준수 하에 진입이 가능합니다.")

st.markdown("---")

# 6. [거래 레이어] 규율 제어 장치
st.subheader("⚡ LAYER 4: TRADING & DISCIPLINE (메타인지 제어)")
st.markdown("⚠️ **포지션 진입 전, 아래 원칙을 반드시 체크하십시오.**")

rule1 = st.checkbox("1. 상위 타임프레임(추세)과 하위 타임프레임(진입)의 방향성 정렬을 확인했는가?")
rule2 = st.checkbox(f"2. 현재 사용하려는 레버리지가 권장 가이드({recommended_lev}x) 이하인가?")
rule3 = st.checkbox("3. 계산된 손절 시 예상 손실 금액을 심리적으로 완전히 받아들였는가?")

if rule1 and rule2 and rule3 and rr_ratio >= 2.0:
    st.success("✅ 모든 매매 규율 및 손익비 조건 통과. 포지션 진입 관제가 허용됩니다.")
else:
    st.error("🔒 진입 제어 장치 활성화: 규율 미준수 또는 손익비 미달로 인해 진입이 차단되었습니다.")
