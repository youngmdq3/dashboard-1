import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 기본 설정 (와이드 모드)
st.set_page_config(page_title="NOIR TRADING OBSERVER", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #111111; color: #ffffff; }
    .sidebar .sidebar-content { background: #1a1a1a; }
    h1, h2, h3 { color: #ffffff !important; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_value=True)

# 2. 사이드바 구성
st.sidebar.title("CONTROL PANEL")
st.sidebar.markdown("---")

market_phase = st.sidebar.selectbox(
    "MARKET PHASE (시장 국면)",
    ["선택하세요", "고변동성 하락장 (리스크 극대화)", "저변동성 횡보장", "강한 추세 상승장"]
)

op_mode = st.sidebar.radio("OPERATION MODE", ["보수형 (Conservative)", "공격형 (Aggressive)"])

st.sidebar.markdown("---")
st.sidebar.markdown("**트레이더 규율 제어**")
st.sidebar.caption("계획되지 않은 진입은 자산의 죽음을 의미한다.")

# 3. 메인 화면 - 타이틀
st.title("🦅 NOIR TRADING SYSTEM : LAYER 1 & 4")
st.markdown("자산운용 가이드 및 매매 규율 관제 탑")
st.markdown("---")

# 4. [운영 레이어] 자산 및 레버리지 자동 계산 로직
st.subheader("📊 LAYER 1: OPERATION (운영 가이드라인)")

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

# 5. [거래 레이어] 규율 제어 장치
st.subheader("⚡ LAYER 4: TRADING & DISCIPLINE (메타인지 제어)")
st.markdown("⚠️ **포지션 진입 전, 아래 원칙을 반드시 체크하십시오.**")

rule1 = st.checkbox("1. 상위 타임프레임(추세)과 하위 타임프레임(진입)의 방향성 정렬을 확인했는가?")
rule2 = st.checkbox(f"2. 현재 사용하려는 레버리지가 권장 가이드({recommended_lev}x) 이하인가?")
rule3 = st.checkbox("3. 손절가(SL)를 시스템에 먼저 입력했는가?")

if rule1 and rule2 and rule3:
    st.success("✅ 모든 매매 규율 통과. 포지션 진입 및 일지 작성이 허용됩니다.")
else:
    st.error("🔒 규율 미준수: 진입 제어 장치가 활성화되어 매매 일지 작성이 차단되었습니다.")
