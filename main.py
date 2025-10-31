import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 대시보드",
    layout="wide",
    page_icon="🎮",
)

# --- CSS 스타일 (다크톤 + 간지) ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3 {
    color: #8c61ff !important;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.7);
}
.stDataFrame, .stExpander {
    background: rgba(20, 20, 40, 0.7);
    border-radius: 12px;
    padding: 10px;
    border: 1px solid rgba(140, 97, 255,0.5);
}
section[data-testid="stSidebar"] {
    background-color: #1e1b4b;
    border-right: 2px solid #302b63;
}
section[data-testid="stSidebar"] * {
    color: #8c61ff !important;
}
div[data-baseweb="select"] > div {
    background-color: #2b2a5f !important;
    border: 1px solid #8c61ff !important;
}
div[data-baseweb="radio"] label {
    color: #8c61ff !important;
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
st.markdown("##### Streamlit + Plotly | Dark Purple & Blue Theme")

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
    st.write("데이터를 바탕으로 인기 게임 분석과 시각화를 진행할 수 있습니다.")

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

    # y축 기본값: Installs 없으면 첫 숫자형 컬럼
    y_axis = "Installs" if "Installs" in numeric_columns else numeric_columns[0]

    chart_type = st.sidebar.radio("그래프 유형", ["막대 그래프", "산점도", "상자그림"])

    st.subheader(f"📊 {chart_type} : {x_axis} vs {y_axis}")

    # --- 그래프 생성 ---
    if chart_type == "막대 그래프":
        df_sorted = df.sort_values(by=y_axis, ascending=False)
        fig = px.bar(
            df_sorted, x=x_axis, y=y_axis, color=y_axis,
            text=y_axis,
            color_continuous_scale=px.colors.sequential.Purples,
            template="plotly_dark"
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    elif chart_type == "산점도":
        fig = px.scatter(
            df, x=x_axis, y=y_axis, color=y_axis,
            color_continuous_scale=px.colors.sequential.Blues,
            template="plotly_dark",
            size=y_axis,
            hover_data=df.columns
        )

    else:  # 상자그림
        fig = px.box(
            df, x=x_axis, y=y_axis, color=y_axis,
            color_continuous_scale=px.colors.sequential.Viridis,
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
        상위 소수 게임이 높은 평점과 다운로드 수를 차지합니다.  
        리뷰 수와 다운로드 수의 상관관계가 강하게 나타납니다.
        """)
