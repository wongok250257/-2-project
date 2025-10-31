import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 대시보드 - Cyberpunk",
    layout="wide",
    page_icon="🎮",
)

# --- CSS: 사이버펑크 스타일 ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    font-family: 'Orbitron', sans-serif;
    color: #ffffff;
}

/* 제목 h1, h2, h3: 네온 스타일 */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff00ff !important;
    text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 20px #00ffff, 0 0 30px #00ffff;
}

/* 일반 텍스트 */
.stMarkdown, .stText, .stDataFrame, div, p, label, span {
    font-family: 'Orbitron', sans-serif;
    color: #f0f9ff !important;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #1a1a2e;
    border-right: 2px solid #ff00ff;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* 드롭다운, 라디오 버튼 */
div[data-baseweb="select"] > div, div[data-baseweb="radio"] label {
    background-color: #ff00ff !important;
    border: 1px solid #00ffff !important;
    color: #ffffff !important;
    font-weight: bold;
}

/* 버튼 네온 스타일 */
.stButton>button {
    background: linear-gradient(45deg, #ff00ff, #00ffff);
    color: white;
    font-weight: bold;
    border: 2px solid #00ffff;
    box-shadow: 0 0 10px #ff00ff, 0 0 20px #00ffff;
    transition: 0.3s;
}
.stButton>button:hover {
    box-shadow: 0 0 20px #ff00ff, 0 0 40px #00ffff, 0 0 60px #ff00ff;
}

/* 그래프 네온 글씨 */
.main .block-container .stPlotlyChart div div svg g text {
    fill: #00ffff !important;
}
</style>
""", unsafe_allow_html=True)

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")

df = load_data()

# --- 제목 ---
st.title("🎮 Android 게임 데이터 대시보드 - Cyberpunk")
st.markdown("##### 네온 + 사이버펑크 스타일 Android 게임 데이터 시각화")

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

# ==============================
# 📊 시각화
# ==============================
with tab2:
    st.sidebar.header("⚙️ 시각화 설정")

    # X축은 Installs만
    x_axis = "Installs"
    y_axis = st.sidebar.selectbox("Y축 (숫자형)", df.select_dtypes(include=['int64','float64']).columns.tolist())

    st.subheader(f"📊 막대 그래프 : {x_axis} vs {y_axis}")

    # 막대 그래프
    df_sorted = df.sort_values(by=y_axis, ascending=False)
    fig = px.bar(
        df_sorted,
        x=x_axis,
        y=y_axis,
        color=x_axis,
        text=y_axis,
        color_discrete_sequence=px.colors.sequential.Plasma,
        template="plotly_dark"
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_axis,
        font=dict(color="#00ffff", family="Orbitron"),
        title_font=dict(color="#ff00ff", family="Orbitron"),
        legend_title_font=dict(color="#ff00ff"),
        legend_font=dict(color="#00ffff"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

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
