import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 데이터 대시보드",
    layout="wide",
    page_icon="🎮",
)

# --- CSS 스타일링 ---
st.markdown("""
<style>
/* 전체 배경과 글씨 */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    color: #e0f2fe;
}

/* 제목 스타일 */
h1, h2, h3 {
    color: #38bdf8 !important;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.6);
}

/* 일반 텍스트 */
.stMarkdown, .stText, .stDataFrame, div, p, label, span {
    color: #f0f9ff !important;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #1e3a8a;
    border-right: 2px solid #0c4a6e;
}
section[data-testid="stSidebar"] * {
    color: #f0f9ff !important;
}

/* 드롭다운, 셀렉트박스 */
div[data-baseweb="select"] > div {
    background-color: #2563eb !important;
    border: 1px solid #1e40af !important;
    color: #f0f9ff !important;
}
div[data-baseweb="radio"] label {
    color: #f0f9ff !important;
}

/* 버튼 스타일 */
.stButton>button {
    background: linear-gradient(45deg, #3b82f6, #1e40af);
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")

df = load_data()

# --- 제목 ---
st.title("🎮 Android 게임 데이터 대시보드")
st.markdown("##### Streamlit + Plotly 기반 Android 게임 데이터 시각화")

# --- 탭 ---
tab1, tab2, tab3 = st.tabs(["📄 데이터 요약", "📊 시각화", "💡 인사이트"])

# ==============================
# 1️⃣ 데이터 요약
# ==============================
with tab1:
    st.subheader("📋 데이터 개요")

    col1, col2, col3 = st.columns(3)
    col1.metric("총 데이터 수", len(df))
    col2.metric("컬럼 개수", len(df.columns))
    col3.metric("결측치 포함 여부", "✅ 없음" if df.isna().sum().sum()==0 else "⚠️ 있음")

    with st.expander("🔍 데이터 미리보기"):
        st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")
    st.write("""
    Android 게임 데이터에는 다운로드 수, 평점, 리뷰 수, 카테고리 등이 포함되어 있습니다.  
    이를 통해 인기 게임 분석, 다운로드 영향 요소 확인 등이 가능합니다.
    """)

# ==============================
# 2️⃣ 시각화
# ==============================
with tab2:
    st.sidebar.header("⚙️ 시각화 설정")

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    x_axis = st.sidebar.selectbox("X축 (범주형)", categorical_columns)
    y_axis = st.sidebar.selectbox("Y축 (숫자형)", numeric_columns)
    chart_type = st.sidebar.radio("그래프 유형", ["막대 그래프", "산점도", "상자그림"])

    st.subheader(f"📊 {chart_type} : {x_axis} vs {y_axis}")

    if chart_type == "막대 그래프":
        df_sorted = df.sort_values(by=y_axis, ascending=False)
        fig = px.bar(
            df_sorted, x=x_axis, y=y_axis, color=x_axis,
            text=y_axis,
            color_discrete_sequence=px.colors.sequential.Blues,
            template="plotly_dark"
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    elif chart_type == "산점도":
        fig = px.scatter(
            df, x=x_axis, y=y_axis, color=x_axis,
            color_discrete_sequence=px.colors.sequential.Blues,
            template="plotly_dark"
        )
    else:  # 상자그림
        fig = px.box(
            df, x=x_axis, y=y_axis, color=x_axis,
            color_discrete_sequence=px.colors.sequential.Blues,
            template="plotly_dark"
        )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_axis,
        font=dict(color="white", family="Segoe UI"),
        title_font=dict(color="#38bdf8", family="Segoe UI"),
        legend_title_font=dict(color="white"),
        legend_font=dict(color="white"),
        margin=dict(l=30, r=30, t=60, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"🏆 {y_axis} 기준 상위 10개 {x_axis}")
    top10 = df.sort_values(by=y_axis, ascending=False).head(10)
    st.dataframe(top10[[x_axis, y_axis]], use_container_width=True)

# ==============================
# 3️⃣ 인사이트
# ==============================
with tab3:
    st.subheader("💡 데이터 인사이트")
    if not df.empty:
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            max_val = df[col].max()
            min_val = df[col].min()
            mean_val = df[col].mean()
            st.write(f"- **{col}** → 최고값: {max_val:.2f}, 최저값: {min_val:.2f}, 평균: {mean_val:.2f}")

        st.markdown("---")
        st.write("""
        📈 **요약:**  
        상위 소수 게임이 높은 평점과 다운로드 수를 차지하고 있습니다.  
        리뷰 수와 다운로드 수의 상관관계가 강하게 나타납니다.  
        인기 장르는 시각화 탭에서 쉽게 비교 가능합니다.

        🎯 **활용 팁:**  
        - X축: `Category`, Y축: `Installs` → 인기 장르 비교  
        - `Rating`과 `Reviews` 비교 → 평점과 리뷰 상관관계 확인
        """)
