import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. 페이지 기본 설정 (와이드 모드 및 타이틀)
st.set_page_config(page_title="OWNER TRADING SYSTEM", layout="wide")

# 무채색 오너 감성을 위한 딥 다크 커스텀 스타일
st.markdown("""
    <style>
    .reportview-container, .main { background-color: #0b0b0b; color: #e0e0e0; }
    .sidebar .sidebar-content { background-color: #121212; }
    h1, h2, h3, h4 { color: #ffffff !important; font-family: 'Courier New', monospace; letter-spacing: 1px; }
    .stButton>button { background-color: #222222; color: white; border: 1px solid #444444; }
    .stButton>button:hover { background-color: #333333; border: 1px solid #ffffff; }
    </style>
""", unsafe_allow_html=True)

# 2. 사이드바 구성 (오너 전용 제어 센터)
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

# 5. [신규 추가] 자산 체급 상승 시뮬레이터 (복리 시각화)
st.subheader("📈 ASSET GROWTH SIMULATOR (자산 성장 시뮬레이션)")
st.markdown("설정한 목표 수익률과 기간에 따른 체급 변화 추이를 시각화합니다.")

sim_col1, sim_col2, sim_col3 = st.columns(3)
with sim_col1:
    target_pct = st.number_input("회전당 목표 수익률 (%)", value=5.0, step=0.5) / 100
with sim_col2:
    total_trades = st.slider("총 매매 횟수 (사이클)", min_value=10, max_value=100, value=30)
with sim_col3:
    agg_multiplier = st.number_input("공격형 모드 가중치 (배수)", value=1.5, step=0.1)

# 복리 계산 로직
trades = np.arange(0, total_trades + 1)
con_growth = current_seed * ((1 + target_pct) ** trades)
agg_growth = current_seed * ((1 + (target_pct * agg_multiplier)) ** trades)

# Plotly 차트 생성 (무채색 스케일 감성 코딩)
fig = go.Figure()
fig.add_trace(go.Scatter(x=trades, y=con_growth, name='보수형 (Base)', line=dict(color='#888888', width=2)))
fig.add_trace(go.Scatter(x=trades, y=agg_growth, name='공격형 (Aggressive)', line=dict(color='#ffffff', width=2.5, dash='dot')))

fig.update_layout(
    title=f"복리 사이클에 따른 자산 추이 (최종 목표 체급: ${agg_growth[-1]:,.0f})",
    xaxis_title="매매 횟수 (Trades)",
    yaxis_title="자산 규모 ($)",
    template="plotly_dark",
    background_color="#121212",
    plot_bgcolor="#121212",
    paper_bgcolor="#0b0b0b",
    margin=dict(l=20, r=20, t=50, b=20)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 6. [거래 레이어] 규율 제어 장치
st.subheader("⚡ LAYER 4: TRADING & DISCIPLINE (메타인지 제어)")
st.markdown("⚠️ **포지션 진입 전, 아래 원칙을 반드시 체크하십시오. 하나라도 누락 시 진입이 차단됩니다.**")

rule1 = st.checkbox("1. 상위 타임프레임(추세)과 하위 타임프레임(진입)의 방향성 정렬을 확인했는가?")
rule2 = st.checkbox(f"2. 현재 사용하려는 레버리지가 권장 가이드({recommended_lev}x) 이하인가?")
rule3 = st.checkbox("3. 손절가(SL)를 시스템에 먼저 입력했는가? (뇌동 손절 절대 금지)")

if rule1 and rule2 and rule3:
    st.success("✅ 모든 매매 규율 통과. 포지션 진입 관제가 허용됩니다.")
else:
    st.error("🔒 규율 미준수: 진입 제어 장치가 활성화되어 매매 통제가 차단되었습니다.")
