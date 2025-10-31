import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 데이터 대시보드 - Cyberpunk",
    layout="wide",
    page_icon="🎮",
)

# --- CSS: 사이버펑크 스타일 ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

/* 전체 배경 */
body {
    background: linear-gradient(135deg, #0a0a0a, #1b1b40, #2a0a5e);
    color: #00ffff;
    font-family: 'Orbitron', sans-serif;
}

/* 제목 h1, h2, h3 */
h1, h2, h3 {
    color: #00ffff !important;
    text-shadow: 0 0 5px #00ffff, 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 30px #00ffff;
    font-family: 'Orbitron', sans-serif !important;
}

/* 일반 텍스트 */
.stMarkdown, .stText, .stDataFrame, div, p, label, span {
    color: #ffffff !important;
    font-family: 'Orbitron', sans-serif;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #1b1b40;
    border-right: 2px solid #00ffff;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* 버튼 네온 스타일 */
.stButton>button {
    background: linear-gradient(45deg, #00ffff, #ff00ff);
    color: white;
    font-weight: bold;
    border: 2px solid #ff00ff;
    box-shadow: 0 0 10px #00ffff, 0 0 20px #ff00ff;
    transition: 0.3s;
}
.stButton>button:hover {
    box-shadow: 0 0 20px #00ffff, 0 0 40px #ff00ff, 0 0 60px #00ffff;
}
</style>
""", unsafe_allow_html=True)

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("android-games.csv")
    # Installs 정수형 변환
    if 'Installs' in df.columns:
        df['Installs'] = df['Installs'].astype(str).str.replace(',','').str.replace('+','').astype(int)
    return df

df = load_data()

# --- 제목 ---
st.title("🎮 Android 게임 데이터 대시보드 - Cyberpunk")
st.markdown("##### 파란색, 보라색, 검정색 사이버펑크 스타일로 Android 게임 데이터를 분석하고 시각화")

# --- 탭 ---
tab1, tab2, tab3 = st.tabs(["📄 데이터 요약", "📊 시각화", "💡 인사이트"])

# ==============================
# 📄 데이터 요약
# ==============================
with tab1:
    st.subheader("📋 데이터 개요")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 데이터 수", len(df))
    col2.metric("컬럼 개수", len(df.columns))
    col3.metric("결측치 포함 여부", "✅ 없음" if df.isna().sum().sum()==0 else "⚠️ 있음")

    with st.expander("🔍 데이터 미리보기"):
        st.dataframe(df.head(), use_container_width=True)

    st.markdown("""
    이 데이터는 Android 게임의 다양한 특성을 포함하고 있습니다.  
    예: 다운로드 수(Installs), 평점(Rating), 리뷰 수(Reviews), 장르(Category) 등.  
    이를 바탕으로 인기 게임 분석, 다운로드에 영향을 주는 요소 탐색, 장르별 비교 등이 가능합니다.
    """)

# ==============================
# 📊 시각화
# ==============================
with tab2:
    st.sidebar.header("⚙️ 시각화 설정")

    # Y축 숫자형 선택
    numeric_columns = df.select_dtypes(include=['int64','float64']).columns.tolist()
    y_axis = st.sidebar.selectbox("Y축 (숫자형)", numeric_columns, index=numeric_columns.index('Rating') if 'Rating' in numeric_columns else 0)

    st.subheader(f"📊 막대 그래프: Installs vs {y_axis}")
    st.markdown("""
    📌 **설명:**  
    - X축: Installs (다운로드 수)  
    - Y축: 선택한 숫자형 컬럼 (예: 평점, 리뷰 수)  
    - 다운로드 수에 따른 앱 성능 비교 및 상위 앱 확인 가능
    """)

    # 막대 그래프
    df_sorted = df.sort_values(by=y_axis, ascending=False).head(50)  # 상위 50개 앱
    fig = px.bar(
        df_sorted,
        x='Installs',
        y=y_axis,
        color='Installs',
        text=y_axis,
        color_continuous_scale=px.colors.sequential.Plasma,
        template="plotly_dark"
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        yaxis_title=y_axis,
        font=dict(color="#00ffff", family="Orbitron"),
        title_font=dict(color="#ff00ff", family="Orbitron"),
        legend_title_font=dict(color="#ff00ff"),
        legend_font=dict(color="#00ffff"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 상위 10개 표시
    st.subheader(f"🏆 {y_axis} 기준 상위 10개 앱")
    top10 = df.sort_values(by=y_axis, ascending=False).head(10)
    st.dataframe(top10[['Installs', y_axis]], use_container_width=True)

# ==============================
# 💡 인사이트
# ==============================
with tab3:
    st.subheader("💡 데이터 인사이트")
    if not df.empty:
        numeric_cols = df.select_dtypes(include=['int64','float64']).columns
        for col in numeric_cols:
            max_val, min_val, mean_val = df[col].max(), df[col].min(), df[col].mean()
            st.write(f"- **{col}** → 최고: {max_val:.2f}, 최저: {min_val:.2f}, 평균: {mean_val:.2f}")

        st.markdown("---")
        st.markdown("""
        📈 **요약:**  
        - 다운로드 수 상위 앱들은 평점과 리뷰 수에서도 높은 경향을 보입니다.  
        - Installs 기준 상위 앱을 통해 인기 게임 트렌드 확인 가능.  
        - 막대 그래프를 통해 앱별 성능 비교 및 마케팅 전략에 활용 가능.  

        🎯 **활용 팁:**  
        - X축: 다운로드 수, Y축: 평점 또는 리뷰 수 설정으로 인기 앱 분석 가능.  
        - 상위 앱 데이터를 활용하여 장르별 트렌드 분석 가능.  
        - 앱 추천, 신규 게임 기획, 마케팅 전략 수립에 활용 가능.
        """)
