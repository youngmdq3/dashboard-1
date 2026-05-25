import streamlit as st

# 1. 페이지 기본 설정 및 모바일 반응형 뷰포트 최적화
st.set_page_config(page_title="OWNER SYSTEM", layout="wide")

# 불필요한 이모지를 배제한 하이엔드 무채색 터미널 스타일 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 톤 다운 */
    .reportview-container, .main, block-container { background-color: #050505; color: #d4d4d4; }
    div[data-testid="stSidebarUserContent"] { background-color: #0c0c0c; }
    
    /* 타이틀 및 텍스트 스타일 정의 */
    h1, h2, h3, h4 { color: #ffffff !important; font-family: 'Courier New', monospace; font-weight: 700; letter-spacing: -0.5px; }
    .small-caption { font-size: 12px; color: #737373; font-family: monospace; }
    
    /* 메트릭 박스 커스텀 (조잡한 기본 디자인 변경) */
    div[data-testid="stMetricKey"] { color: #a3a3a3 !important; font-size: 13px !important; font-weight: 500; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 24px !important; font-weight: 700; font-family: 'Courier New', monospace; }
    
    /* 경고창 및 구분선 스타일 */
    hr { border-color: #262626 !important; }
    div.stAlert { background-color: #171717; border: 1px solid #262626; color: #e5e5e5; border-radius: 0px; }
    </style>
""", unsafe_allow_html=True)

# 2. 제어 센터 (사이드바 - 입력값 통제)
st.sidebar.markdown("### SYSTEM INPUT")
market_phase = st.sidebar.selectbox(
    "MARKET PHASE",
    ["저변동성 횡보장", "고변동성 하락장 (리스크 관리)", "강한 추세 상승장"]
)
op_mode = st.sidebar.radio("OPERATION MODE", ["보수형 (Conservative)", "공격형 (Aggressive)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ACCOUNT INPUT")
total_assets = st.sidebar.number_input("총 순자산 (Net Assets, $)", value=10000, step=1000)
current_leverage_amt = st.sidebar.number_input("현재 총 포지션 금액 (Opened Position, $)", value=15000, step=1000)


# 3. 메인 레이아웃 - 타이틀
st.title("OWNER CAPITAL MANAGEMENT SYSTEM")
st.markdown("<p class='small-caption'>CORE LAYER 1: TOTAL CAPITAL OPERATION STATUS</p>", unsafe_allow_html=True)
st.markdown("---")


# 4. 자산 운영 상태 연산 로직
# 시장 국면 및 운영 모드별 권장 레버리지 설정
if market_phase == "고변동성 하락장 (리스크 관리)":
    rec_lev = 1.0 if op_mode == "보수형 (Conservative)" else 2.0
elif market_phase == "강한 추세 상승장":
    rec_lev = 3.0 if op_mode == "보수형 (Conservative)" else 5.0
else:
    rec_lev = 1.5 if op_mode == "보수형 (Conservative)" else 3.0

# 배분 비율 및 차이 계산
current_lev_ratio = current_leverage_amt / total_assets if total_assets > 0 else 0.0
lev_difference = rec_lev - current_lev_ratio

# 추가 지표 계산 (자본 가동률 및 여유 여력)
max_allowed_position = total_assets * rec_lev
remaining_margin = max_allowed_position - current_leverage_amt
capital_utilization = (current_leverage_amt / max_allowed_position) * 100 if max_allowed_position > 0 else 0.0


# 5. 대시보드 메트릭 출력 (모바일 가독성 최적화 배치)
st.markdown("### ACCOUNT METRICS")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="총 순자산 (SEED)", value=f"${total_assets:,.0f}")
    st.metric(label="현재 총 포지션 (LEVERAGE AMT)", value=f"${current_leverage_amt:,.0f}")

with col2:
    st.metric(label="현재 레버리지 비율 (CURRENT LEV)", value=f"{current_lev_ratio:.2f}x")
    st.metric(label="권장 레버리지 비율 (
