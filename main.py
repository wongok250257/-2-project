import streamlit as st
import pandas as pd
import plotly.express as px

# --- 기본 설정 ---
st.set_page_config(
    page_title="Android 게임 데이터 시각화",
    layout="wide",
    page_icon="🎮",
)

# --- CSS 스타일 커스터마이징 ---
st.markdown("""
    <style>
    /* 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
    }
    /* 제목 스타일 */
    h1, h2, h3 {
        color: #38bdf8 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    /* 데이터프레임 투명 배경 */
    .stDataFrame {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    /* 사이드바 배경 및 글씨 */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 2px solid #334155;
        color: white;
    }
    /* 사이드바 내 텍스트, 라벨, 버튼, 셀렉트박스 글자색 */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    /* selectbox, radio 버튼 등 테두리 */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    div[data-baseweb="radio"] label {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 제목 영역 ---
st.title("🎮 Android 게임 데이터 대시보드")
st.markdown("##### Plotly + Streamlit을 활용한 데이터 시각화 앱")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("android-games.csv")
    return df

df = load_data()

# --- 데이터 미리보기 ---
st.subheader("📋 데이터 미리보기")
st.dataframe(df.head(), use_container_width=True)

# --- 사이드바 ---
st.sidebar.header("⚙️ 시각화 설정")

numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

x_axis = st.sidebar.selectbox("X축 (범주형)", categorical_columns)
y_axis = st.sidebar.selectbox("Y축 (숫자형)", numeric_columns)

chart_type = st.sidebar.radio(
    "그래프 유형",
    ["막대 그래프", "산점도", "상자그림", "히스토그램"]
)

# --- Plotly 그래프 ---
st.subheader(f"📈 {chart_type} : {x_axis} vs {y_axis}")

if chart_type == "막대 그래프":
    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis,
                 title=f"{x_axis}별 {y_axis} 비교",
                 template="plotly_dark")
elif chart_type == "산점도":
    fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis,
                     title=f"{x_axis} vs {y_axis}",
                     template="plotly_dark")
elif chart_type == "상자그림":
    fig = px.box(df, x=x_axis, y=y_axis, color=x_axis,
                 title=f"{x_axis}별 {y_axis} 분포",
                 template="plotly_dark")
else:
    fig = px.histogram(df, x=y_axis, color=x_axis,
                       title=f"{y_axis} 분포 (by {x_axis})",
                       template="plotly_dark")

fig.update_layout(
    margin=dict(l=30, r=30, t=60, b=30),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

# --- 통계 요약 ---
with st.expander("📊 기본 통계 보기"):
    st.write(df.describe())
