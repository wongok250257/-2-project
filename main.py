import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="🎮 Android 게임 데이터 대시보드",
    layout="wide",
    page_icon="🎮",
)

# --- CSS 스타일 ---
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 색상 */
    .stApp {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
    }

    /* 제목 색상 */
    h1, h2, h3 {
        color: #38bdf8 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }

    /* 모든 텍스트를 흰색으로 통일 */
    .stMarkdown, .stText, .stDataFrame, div, p, label, span {
        color: white !important;
    }

    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 2px solid #334155;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* 드롭다운, 라디오 버튼, 셀렉트박스 배경 */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    div[data-baseweb="radio"] label {
        color: white !important;
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
st.markdown("##### Streamlit + Plotly를 활용한 Android 게임 데이터 시각화")

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
    예를 들어 다운로드 수, 평점, 리뷰 수, 카테고리 등의 정보가 있습니다.  
    이를 바탕으로 어떤 게임이 인기가 많은지, 어떤 요소가 다운로드에 영향을 주는지 등을 분석할 수 있습니다.
    """)

# ==============================
# 📊 2. 시각화 탭
# ==============================
with tab2:
    st.sidebar.header("⚙️ 시각화 설정")

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    # ✅ X축만 선택하도록 변경 (title 제거)
    x_axis_options = [col for col in categorical_columns if col.lower() != "title"]
    x_axis = st.sidebar.selectbox("X축 (범주형)", x_axis_options)

    y_axis = "Installs" if "Installs" in numeric_columns else numeric_columns[0]  # 기본값 자동 선택

    chart_type = st.sidebar.radio("그래프 유형", ["막대 그래프", "산점도", "상자그림"])

    st.subheader(f"📊 {chart_type} : {x_axis} vs {y_axis}")

    # --- 그래프 종류별 생성 ---
    if chart_type == "막대 그래프":
        df_sorted = df.sort_values(by=y_axis, ascending=False)
        fig = px.bar(
            df_sorted, x=x_axis, y=y_axis, color=x_axis,
            text=y_axis,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_white"
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    elif chart_type == "산점도":
        fig = px.scatter(
            df, x=x_axis, y=y_axis, color=x_axis,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_white"
        )

    else:  # 상자그림
        fig = px.box(
            df, x=x_axis, y=y_axis, color=x_axis,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_white"
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
        전체적으로 상위 소수의 게임이 높은 평점과 다운로드 수를 차지하고 있습니다.  
        리뷰 수와 다운로드 수의 상관관계가 강하게 나타나는 경향이 있으며,  
        인기 장르는 그래프에서 선택적으로 비교해볼 수 있습니다.  

        🎯 **활용 팁:**  
        - X축을 `Category`로 두면 인기 장르를 쉽게 비교할 수 있습니다.  
        - `Rating`과 `Reviews`를 비교하면 평점과 리뷰의 상관관계를 시각적으로 확인할 수 있습니다.
        """)
