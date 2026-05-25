# ==============================================================================
# 4. LAYER 1: OPERATION (전체 자산 운영 현황 및 체급 모니터링)
# ==============================================================================
st.subheader("LAYER 1: CAPITAL OPERATION STATUS")
st.markdown("<p class='system-sub-caption'>Account Level Asset Allocation & Leverage Variance</p>", unsafe_allow_html=True)

# 메인 화면 자산 입력 구역 (모바일 터치 가독성 최적화)
col_in1, col_in2 = st.columns(2)
with col_in1:
    total_assets = st.number_input("총 순자산 입력 (Net Assets, $)", value=10000, step=1000)
with col_in2:
    current_lev_ratio = st.number_input("현재 계정 전체 실행 레버리지 배수 (Current Account Leverage, x)", value=1.0, step=0.1)

# 로직 연산: 국면별 권장 레버리지 도출
if market_phase == "고변동성 하락장 (리스크 관리)":
    rec_lev = 1.0 if op_mode == "보수형 (Conservative)" else 2.0
elif market_phase == "강한 추세 상승장":
    rec_lev = 3.0 if op_mode == "보수형 (Conservative)" else 5.0
else:
    rec_lev = 1.5 if op_mode == "보수형 (Conservative)" else 3.0

# 자산 지표 연산
current_leverage_amt = total_assets * current_lev_ratio
lev_difference = rec_lev - current_lev_ratio
max_allowed_position = total_assets * rec_lev
remaining_margin = max_allowed_position - current_leverage_amt
capital_utilization = (current_lev_ratio / rec_lev) * 100 if rec_lev > 0 else 0.0

# 자산 체급(Tier) 분류 로직
if total_assets >= 1000000:
    current_tier = "TIER 1 (INSTITUTIONAL MASTER)"
    next_tier_txt = "MAX TIER"
    tier_progress = 100.0
elif total_assets >= 100000:
    current_tier = "TIER 2 (MACRO ALLOCATOR)"
    next_tier_txt = "$1,000,000"
    tier_progress = (total_assets / 1000000) * 100
elif total_assets >= 30000:
    current_tier = "TIER 3 (GROWTH ACCELERATOR)"
    next_tier_txt = "$100,000"
    tier_progress = (total_assets / 100000) * 100
else:
    current_tier = "TIER 4 (SEED BUILDER)"
    next_tier_txt = "$30,000"
    tier_progress = (total_assets / 30000) * 100

# 메트릭 출력 구역
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="총 순자산 (SEED)", value=f"${total_assets:,.0f}")
    st.metric(label="현재 가동 자본 (LEVERAGE AMT)", value=f"${current_leverage_amt:,.0f}")
with col_m2:
    st.metric(label="현재 레버리지 (CURRENT LEV)", value=f"{current_lev_ratio:.2f}x")
    st.metric(label="권장 레버리지 (REC LEV)", value=f"{rec_lev:.1f}x")
with col_m3:
    status_text = f"+{lev_difference:.2f}x 여유" if lev_difference >= 0 else f"{abs(lev_difference):.2f}x 초과 (위험)"
    st.metric(label="레버리지 격차 (VARIANCE)", value=status_text)
    st.metric(label="자본 가동률 (UTILIZATION)", value=f"{capital_utilization:.1f}%")

# Layer 1 시스템 평가창 (f-string 문법 에러 완벽 수정 및 가독성 확보)
st.markdown("<br>", unsafe_allow_html=True)
l1_col1, l1_col2 = st.columns(2)
with l1_col1:
    st.markdown(f"""
        <div class="terminal-block">
        <strong>[CAPITAL TIER MONITOR]</strong><br>
        • ACTIVE TIER : {current_tier}<br>
        • NEXT TIER GOAL : {next_tier_txt}<br>
        • TIER PROGRESS : {tier_progress:.1f}%
        </div>
    """, unsafe_allow_html=True)
with l1_col2:
    if lev_difference < 0:
        st.markdown(f"""
            <div style="padding:15px; background-color:#1a0505; border:1px solid #551a1a; color:#f87171; font-family:monospace; font-size:13px; height:100%;">
            <strong>[CRITICAL SYSTEM ALERT] OVER-LEVERAGED STATUS</strong><br>
            현재 전체 자본 가이드라인의 임계치를 초과하여 운용 중입니다. 포지션 청산 및 리스크 리듀싱이 필요합니다.<br>
            • 초과 리스크 규모: ${abs(remaining_margin):,.0f}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="padding:15px; background-color:#051a05; border:1px solid #1a551a; color:#4ade80; font-family:monospace; font-size:13px; height:100%;">
            <strong>[OPERATIONAL STABILITY] SYSTEM NORMAL</strong><br>
            계정이 자본 가이드라인 범위 내에서 안전하게 제어되고 있습니다.<br>
            • 추가 진입 가능 여력 (CAPITAL MARGIN): ${remaining_margin:,.0f}
            </div>
        """, unsafe_allow_html=True)
