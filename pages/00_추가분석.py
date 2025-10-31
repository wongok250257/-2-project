import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📈 추가 분석", page_icon="📈")

st.title("📈 추가 분석 페이지")

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")

df = load_data()

# 간단한 시각화 예시
st.subheader("장르별 평균 평점")
fig = px.bar(
    df.groupby("Category")["Rating"].mean().reset_index(),
    x="Category", y="Rating",
    color="Category",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig, use_container_width=True)
