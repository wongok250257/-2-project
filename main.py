import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 데이터 대시보드",
    layout="wide",
    page_icon="🎮",
)

# --- CSS 스타일 (간지나게 꾸미기) ---
st.markdown("""
<style>
/* 전체 배경 */
.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 제목 스타일 */
h1, h2, h3 {
    color: #00f0ff !important;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.6);
}

/* 카드 느낌 박스 */
.stDataFrame, .stExpander {
    background: rgba(0, 0, 0, 0.4);
    border-radius: 12px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* 사이드바 스타일 */
section[data-testid="stSidebar"] {
    background-color: #1a2a3a;
    border-right: 2px solid #334155;
}
section[data-testid="stSidebar"] * {
    color: #00f0ff !important;
}

/* 드롭다운, 라디오 버튼 */
div[data-baseweb="select"] > div {
    background-color: #203a43 !important;
    border: 1px solid #00f0ff !important;
}
div[data-baseweb="radio"] label {
    color: #00f0ff !important;
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
st.markdown("##### Streamlit + Plotly로 만든 간지나는 Android 게임 시각화")

# --- 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["📄 데이터 요약", "📊 시각화", "💡 인사이트"])

# ==============================
# 📄 1. 데이터 요약 탭
# ==============================
with tab1:
    st.subheader("📋 데이터 개요")

    col1, col2, col3 = st.columns(3)
    col1.metric("총 데이터 수", len(df))
    col2.metric("컬럼 개수", len(df.columns))
    col3.metric("결측치 포함 여부", "✅ 없음" if df.isna().sum().sum() == 0 else "⚠️ 있음")

    with st.expander("🔍 데이터 미리보기"):
        st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")
    st.write("""
    이 데이터는 Android 게임의 다양한 특성을 포함하고 있습니다.  
    다운로드 수, 평점, 리뷰 수, 카테고리 등의 정보를 기반으로 인기 게임 분석 가능.
    """)

# ==============================
# 📊 2. 시각화 탭
# ==============================
with tab2:
    st.sidebar.header("⚙️ 시각화 설정")

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    # title 컬럼 제외
    x_axis_options = [col for col in categorical_columns if col.lower() != "title"]
    x_axis = st.sidebar.selectbox("X축 (범주형)", x_axis_options)

    y_axis = "Installs" if "Installs" in numeric_columns else numeric_columns[0]

    chart_type = st.sidebar.radio("그래프 유형", ["막대 그래프", "산점도", "상자그림"])

    st.subheader(f"📊 {chart_type} : {x_axis} vs {y_axis}")

    # --- 그래프 생성 ---
    if chart_type == "막대 그래프":
        df_sorted = df.sort_values(by=y_axis, ascending=False)
        fig = px.bar(
            df_sorted, x=x_axis, y=y_axis, color=y_axis,
            text=y_axis,
            color_continuous_scale=px.colors.sequential.Turbo,
            template="plotly_dark"
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    elif chart_type == "산점도":
        fig = px.scatter(
            df, x=x_axis, y=y_axis, color=y_axis,
            color_continuous_scale=px.colors.sequential.Viridis,
            template="plotly_dark",
            size=y_axis,
            hover_data=df.columns
        )

    else:  # 상자그림
        fig = px.box(
            df, x=x_axis, y=y_axis, color=y_axis,
            color_continuous_scale=px.colors.sequential.Plasma,
            template="plotly_dark"
        )

    # --- 그래프 스타일 ---
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=y_axis,
        font=dict(color="white"),
        title_font=dict(color="white"),
        legend_title_font=dict(color="white"),
        legend_font=dict(color="white"),
        margin=dict(l=30, r=30, t=60, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 상위 10개 ---
    st.subheader(f"🏆 {y_axis} 기준 상위 10개 {x_axis}")
    top10 = df.sort_values(by=y_axis, ascending=False).head(10)
    st.dataframe(top10[[x_axis, y_axis]], use_container_width=True)

# ==============================
# 💡 3. 인사이트 탭
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
        상위 소수의 게임이 높은 평점과 다운로드 수를 차지합니다.  
        리뷰 수와 다운로드 수의 상관관계가 강하게 나타나며,  
        인기 장르는 그래프에서 쉽게 비교 가능.

        🎯 **팁:**  
        - X축을 `Category`로 두면 인기 장르 비교 가능  
        - `Rating`과 `Reviews`를 비교하면 평점과 리뷰 관계 확인 가능
        """)
