import streamlit as st
import pandas as pd
import plotly.express as px

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")

df = load_data()

# --- 컬럼 존재 여부 확인 ---
required_cols = ["Category", "Title", "Installs", "Rating"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    st.error(f"데이터에 다음 컬럼이 없습니다: {missing_cols}")
    st.stop()

# --- 카테고리 선택 ---
categories = df["Category"].unique()
selected_cat = st.selectbox("비교할 카테고리 선택", options=categories)

# --- 선택한 카테고리 내 상위 게임 ---
if selected_cat:
    top_games = df[df["Category"] == selected_cat].sort_values(by="Installs", ascending=False).head(10)

    st.subheader(f"{selected_cat} 카테고리 상위 10 게임 비교")
    st.dataframe(top_games[["Title", "Installs", "Rating"]], use_container_width=True)

    # --- 상위 게임 막대 그래프 ---
    fig = px.bar(
        top_games,
        x="Title",
        y="Installs",
        color="Rating",
        color_continuous_scale=px.colors.sequential.Plasma,
        text="Installs",
        template="plotly_dark"
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Installs",
        margin=dict(l=20, r=20, t=50, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
