import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 대시보드",
    layout="wide",
    page_icon="🎮",
)

# --- CSS: 게임 UI 느낌 ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #4c1d95);
    font-family: 'Orbitron', 'Segoe UI', sans-serif;
    color: #ffffff;
}

/* 제목 */
h1, h2, h3 {
    color: #00f0ff !important;
    text-shadow: 2px 2px 8px #7f00ff;
    font-family: 'Press Start 2P', cursive !important;
}

/* 일반 텍스트 */
.stMarkdown, .stText, .stDataFrame, div, p, label, span {
    color: #f0f9ff !important;
}

/* 탭 배경 카드 느낌 */
.css-1d391kg {  /* Streamlit 탭 */
    background-color: rgba(0,0,0,0.5);
    border-radius: 15px;
    padding: 10px;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #1e3a8a;
    border-right: 2px solid #4c1d95;
    color: #ffffff;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* 드롭다운, 라디오 */
div[data-baseweb="select"] > div, div[data-baseweb="radio"] label {
    background-color: #2563eb !important;
    border: 1px solid #4c1d95 !important;
    color: #ffffff !important;
    font-weight: bold;
}

/* 버튼 네온 느낌 */
.stButton>button {
    background: linear-gradient(45deg, #00f0ff, #7f00ff);
    color: white;
    font-weight: bold;
    border: 2px solid #ffffff;
    box-shadow: 0 0 15px #00f0ff;
}
</style>
""", unsafe_allow_html=True)

# --- 데이터 ---
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")
df = load_data()

# --- 제목 ---
st.title("🎮 Android 게임 데이터 대시보드")
st.markdown("##### 게임 느낌으로 보는 Android 게임 데이터 시각화")

# --- 탭 ---
tab1, tab2, tab3 = st.tabs(["📄 데이터 요약", "📊 시각화", "💡 인사이트"])

# ==============================
# 데이터 요약
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
# 시각화
# ==============================
with tab2:
    st.sidebar.header("⚙️ 시각화 설정")
    numeric_columns = df.select_dtypes(include=['int64','float64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    x_axis = st.sidebar.selectbox("X축 (범주형)", categorical_columns)
    y_axis = st.sidebar.selectbox("Y축 (숫자형)", numeric_columns)
    chart_type = st.sidebar.radio("그래프 유형", ["막대 그래프", "산점도", "상자그림"])

    st.subheader(f"📊 {chart_type} : {x_axis} vs {y_axis}")

    if chart_type == "막대 그래프":
        df_sorted = df.sort_values(by=y_axis, ascending=False)
        fig = px.bar(df_sorted, x=x_axis, y=y_axis, color=x_axis,
                     text=y_axis,
                     color_discrete_sequence=px.colors.sequential.Blues,
                     template="plotly_dark")
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    elif chart_type == "산점도":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis,
                         color_discrete_sequence=px.colors.sequential.Blues,
                         template="plotly_dark")
    else:
        fig = px.box(df, x=x_axis, y=y_axis, color=x_axis,
                     color_discrete_sequence=px.colors.sequential.Blues,
                     template="plotly_dark")

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_axis,
        font=dict(color="#ffffff", family="Orbitron"),
        title_font=dict(color="#00f0ff", family="Press Start 2P"),
        legend_title_font=dict(color="#ffffff"),
        legend_font=dict(color="#ffffff"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# 인사이트
# ==============================
with tab3:
    st.subheader("💡 데이터 인사이트")
    if not df.empty:
        numeric_cols = df.select_dtypes(include=['int64','float64']).columns
        for col in numeric_cols:
            max_val, min_val, mean_val = df[col].max(), df[col].min(), df[col].mean()
            st.write(f"- **{col}** → 최고: {max_val:.2f}, 최저: {min_val:.2f}, 평균: {mean_val:.2f}")
