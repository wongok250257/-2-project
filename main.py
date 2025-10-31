import streamlit as st
import pandas as pd
import plotly.express as px

# 앱 제목
st.set_page_config(page_title="Android 게임 데이터 시각화", layout="wide")
st.title("📊 Android 게임 데이터 시각화 (Plotly + Streamlit)")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("android-games.csv")
    return df

df = load_data()

st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 컬럼 선택
st.sidebar.header("⚙️ 시각화 설정")
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

x_axis = st.sidebar.selectbox("X축 (범주형)", categorical_columns)
y_axis = st.sidebar.selectbox("Y축 (숫자형)", numeric_columns)

# 그래프 유형 선택
chart_type = st.sidebar.radio(
    "그래프 유형 선택",
    ["막대 그래프", "산점도", "상자그림", "히스토그램"]
)

# 그래프 생성
st.subheader(f"📈 {chart_type} - {x_axis} vs {y_axis}")

if chart_type == "막대 그래프":
    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, title=f"{x_axis}별 {y_axis} 비교")
elif chart_type == "산점도":
    fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, title=f"{x_axis} vs {y_axis}")
elif chart_type == "상자그림":
    fig = px.box(df, x=x_axis, y=y_axis, color=x_axis, title=f"{x_axis}별 분포")
else:
    fig = px.histogram(df, x=y_axis, color=x_axis, title=f"{y_axis} 분포 (by {x_axis})")

st.plotly_chart(fig, use_container_width=True)

# 통계 정보
st.subheader("📊 기본 통계 요약")
st.write(df.describe())
