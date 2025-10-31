import streamlit as st
import pandas as pd
import plotly.express as px

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")

df = load_data()

# --- 컬럼 이름 확인 ---
st.write("컬럼 리스트:", df.columns.tolist())

# --- Category별 Rating 평균 ---
if "Category" in df.columns and "Rating" in df.columns:
    cat_rating = df.groupby("Category", as_index=False)["Rating"].mean()
    st.subheader("카테고리별 평균 Rating")
    st.dataframe(cat_rating.sort_values(by="Rating", ascending=False))
else:
    st.warning("Category 또는 Rating 컬럼이 존재하지 않습니다. 컬럼명을 확인하세요.")

# --- Category별 Installs 합계 ---
if "Category" in df.columns and "Installs" in df.columns:
    cat_installs = df.groupby("Category", as_index=False)["Installs"].sum()
    st.subheader("카테고리별 총 다운로드수")
    st.dataframe(cat_installs.sort_values(by="Installs", ascending=False))
else:
    st.warning("Category 또는 Installs 컬럼이 존재하지 않습니다. 컬럼명을 확인하세요.")

# --- 인기 게임 비교 (예시: 특정 Category top5) ---
selected_cat = st.selectbox("비교할 카테고리 선택", options=df["Category"].unique() if "Category" in df.columns else [])
if selected_cat and "Installs" in df.columns:
    top_games = df[df["Category"]==selected_cat].sort_values(by="Installs", ascending=False).head(5)
    st.subheader(f"{selected_cat} 카테고리 상위 5 게임")
    st.dataframe(top_games[["Title", "Installs", "Rating"]] if "Title" in df.columns else top_games)
