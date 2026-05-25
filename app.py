import streamlit as st

# 1. 페이지 기본 설정 및 모바일 뷰포트 최적화
st.set_page_config(page_title="OWNER SYSTEM", layout="wide")

# 하이엔드 무채색 터미널 스타일 CSS (모바일 입력창 가독성 강화)
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 톤 다운 */
    .reportview-container, .main, block-container { background-color: #050505; color: #d4d4d4; }
    div[data-testid="stSidebarUserContent"] { background-color: #0c0c0c; }
    
    /* 타이틀 및 텍스트 스타일 정의 */
    h1, h2, h3, h4 { color: #ffffff !important; font-family: 'Courier New', monospace; font-weight: 700; letter-spacing: -0.5px; }
    .small-caption { font-size: 12px; color: #737373; font-family: monospace; }
    
    /* 메인 화면 입력창(Number Input) 스타일 커스텀 */
    div[data-testid="stNumberInput"] label { color: #a3a3a3 !important; font-size: 13px !important; font-weight: 600; }
    div[data-testid="stNumberInput"] input { background-color: #121212 !important; color: #ffffff !important; border: 1px solid #262626 !important; font-family: 'Courier New', monospace; }
    
    /* 메트릭 박스 커스텀 */
    div[data-testid="stMetricKey"] { color: #a3a3a3 !important; font-size: 13px !important; font-weight: 500; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 24px !important; font-weight: 700; font-family: 'Courier New', monospace; }
    
    /* 경고창 및 구분선 스타일 */
    hr { border-color: #262626 !important; }
    div.stAlert { background-color: #171717; border: 1px solid #262626; color: #e5e5e5; border-radius: 0px; }
    </style>
""", unsafe_allow_html=True)

# 2. 제어 센터 (사이드바 - 환경 제어만 남김)
st.sidebar.markdown("### SYSTEM ENVIRONMENT")
market_phase = st.sidebar.selectbox(
    "MARKET PHASE",
    ["저변동성 횡보장", "고변동성 하락장 (리스크 관리)", "강한 추세 상승장"]
)
op_mode = st.sidebar.radio("OPERATION MODE", ["보수형 (Conservative)", "공격형 (Aggressive)"])


# 3. 메인 레이아웃 - 타이틀
st.title("OWNER CAPITAL MANAGEMENT SYSTEM")
st.markdown("<p class='small-caption'>CORE LAYER 1: TOTAL CAPITAL OPERATION STATUS</p>", unsafe_allow_html=True)
st.markdown("---")


# 4. [수정 방향] 대시보드 메인 입력 매트릭스 (MAIN INPUT LAYER)
st.markdown("### 1. CAPITAL INPUT (메인 자산 입력)")
input_col1, input_col2 = st.columns(2)

with input_col1:
    total_assets = st.number_input("총 순자산 입력 (Net Assets, $)", value=10000, step=1000)

with input_col2:
    current_lev_ratio = st.number_input("현재 실행 중인 레버리지 배수 입력 (Current Leverage, x)", value=1.5, step=0.1)

st.markdown("---")


# 5. 자산 운영 상태 실시간 연산 로직
# 시장 국면 및 운영 모드별 권장 레버리지 결정
if market_phase == "고변동성 하락장 (리스크 관리)":
    rec_lev = 1.0 if op_mode == "보수형 (Conservative)" else 2.0
elif market_phase == "강한 추세 상승장":
    rec_lev = 3.0 if op_mode == "보수형 (Conservative)" else 5.0
else:
    rec_lev = 1.5 if op_mode == "보수형 (Conservative)" else 3.0

# 입력받은 자산과 레버리지 배수를 기반으로 금액 및 격차 역산
current_leverage_amt = total_assets * current_lev_ratio
lev_difference = rec_lev - current_lev_ratio

max_allowed_position = total_assets * rec_lev
remaining_margin = max_allowed_position - current_leverage_amt
capital_utilization = (current_lev_ratio / rec_lev) * 100 if rec_lev > 0 else 0.0


# 6. 대시보드 메트릭 출력 (모바일 최적화 계기판)
st.markdown("### 2. ACCOUNT METRICS (실시간 연산 결과)")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="총 순자산 (SEED)", value=f"${total_assets:,.0f}")
    st.metric(label="현재 총 포지션 금액 (LEVERAGE AMT)", value=f"${current_leverage_amt:,.0f}")

with col2:
    st.metric(label="현재 레버리지 비율 (CURRENT LEV)", value=f"{current_lev_ratio:.2f}x")
    st.metric(label="권장 레버리지 비율 (REC LEV)", value=f"{rec_lev:.1f}x")

with col3:
    if lev_difference >= 0:
        status_text = f"+{lev_difference:.2f}x 여유"
    else:
        status_text = f"{abs(lev_difference):.2f}x 초과 (위험)"
        
    st.metric(label="레버리지 격차 (VARIANCE)", value=status_text)
    st.metric(label="현재 자본 가동률 (UTILIZATION)", value=f"{capital_utilization:.1f}%")

st.markdown("---")


# 7. 리스크 관리 가이드라인 및 여유 여력 통제
st.markdown("### 3. CAPITAL EVALUATION")

if lev_difference < 0:
    st.markdown(
        f"""
        <div style="padding:15px; background-color:#1a0505; border:1px solid #551a1a; color:#f87171; font-family:monospace; font-size:14px;">
        <strong>[CRITICAL WARNING] OVER-LEVERAGED STATUS</strong><br>
        현재 계정이 권장 리스크 한도를 초과하여 오버 레버리지 상태입니다. 포지션을 축소하십시오.<br>
        • 초과 포지션 규모: ${abs(remaining_margin):,.0f}
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div style="padding:15px; background-color:#051a05; border:1px solid #1a551a; color:#4ade80; font-family:monospace; font-size:14px;">
        <strong>[STABLE] OPERATIONAL MARGIN AVAILABLE</strong><br>
        현재 자산 가이드라인 범위 내에서 안전하게 제어되고 있습니다.<br>
        • 추가 진입 가능 여력 (CAPITAL MARGIN): ${remaining_margin:,.0f}
        </div>
        """, 
        unsafe_allow_html=True
    )
