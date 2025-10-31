import streamlit as st
import pandas as pd
import plotly.express as px

# --- 기본 설정 ---
st.set_page_config(
    page_title="Android 게임 데이터 시각화",
    layout="wide",
    page_icon="🎮",
)

# --- CSS 스타일 ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 2px solid #334155;
        color: white;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    div[data-baseweb="radio"] label {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 제목 ---
st.title("🎮 Android 게임 데이터 대시보드")
st.markdown("##### Plotly + Streamlit으로 만드는 게임 데이터 시각화")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")

df = load_data()

# --- 기본 정보 표시 ---
st.subheader("📄 데이터 개요")
col1, col2, col3 = st.columns(3)
col1.metric("총 데이터 개수", len(df))
col2.metric("컬럼 수", len(df.columns))
col3.metric("결측치 포함 여부", "✅ 없음" if df.isna().sum().sum() == 0 else "⚠️ 있음")

st.write("**데이터 컬럼 목록:**", ", ".join(df.columns))

# --- 미리보기 ---
with st.expander("📋 데이터 미리보기 (클릭하여 보기)"):
    st.dataframe(df.head(), use_container_width=True)

# --- 사이드바 ---
st.sidebar.header("⚙️ 시각화 설정")

numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

x_axis = st.sidebar.selectbox("X축 (범주형)", categorical_columns)
y_axis = st.sidebar.selectbox("Y축 (숫자형)", numeric_columns)

chart_type = st.sidebar.radio(
    "그래프 유형 선택",
    ["막대 그래프", "산점도", "상자그림"]
)

# --- 그래프 생성 ---
st.subheader(f"📊 {chart_type} : {x_axis} vs {y_axis}")

if chart_type == "막대 그래프":
    df_sorted = df.sort_values(by=y_axis, ascending=False)
    fig = px.bar(
        df_sorted, x=x_axis, y=y_axis, color=x_axis,
        text=y_axis,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_white",
        title=f"{x_axis}별 {y_axis} 비교"
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
elif chart_type == "산점도":
    fig = px.scatter(
        df, x=x_axis, y=y_axis, color=x_axis,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_white",
        title=f"{x_axis} vs {y_axis}"
    )
elif chart_type == "상자그림":
    fig = px.box(
        df, x=x_axis, y=y_axis, color=x_axis,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_white",
        title=f"{x_axis}별 {y_axis} 분포"
    )

fig.update_layout(
    xaxis_title=None,
    yaxis_title=y_axis,
    margin=dict(l=30, r=30, t=60, b=30),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

# --- 추가 섹션 : 상위 10개 데이터 ---
st.subheader(f"🏆 {y_axis} 기준 상위 10개 {x_axis}")
top10 = df.sort_values(by=y_axis, ascending=False).head(10)
st.dataframe(top10[[x_axis, y_axis]], use_container_width=True)

# --- 간단한 인사이트 출력 ---
st.subheader("💡 데이터 인사이트")
if not df.empty:
    max_val = df[y_axis].max()
    max_item = df.loc[df[y_axis].idxmax(), x_axis]
    st.write(f"➡️ **'{max_item}'** 이(가) `{y_axis}` 값이 가장 높습니다. (최대값: **{max_val}**)")

st.markdown("---")
st.markdown("📊 **Tip:** 사이드바에서 축을 바꾸면 다양한 관계를 바로 시각화할 수 있습니다.")
