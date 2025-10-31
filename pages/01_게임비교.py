import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="🧩 게임 비교", page_icon="🧩")

st.title("🧩 게임 비교 페이지")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    return pd.read_csv("android-games.csv")

df = load_data()

# --- 게임 선택 ---
games = df["App"].dropna().unique().tolist()
selected_games = st.multiselect("비교할 게임을 선택하세요", games[:200], max_selections=3)

if selected_games:
    compare_df = df[df["App"].isin(selected_games)]
    st.subheader("📊 선택한 게임 비교 결과")

    # --- 레이더 차트 (Rating, Reviews, Installs 등 비교) ---
    numeric_features = ["Rating", "Reviews", "Installs", "Price"]
    available_features = [col for col in numeric_features if col in df.columns]

    if available_features:
        fig = go.Figure()

        for game in selected_games:
            values = compare_df[compare_df["App"] == game][available_features].mean().tolist()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=available_features,
                fill='toself',
                name=game
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, color="white")),
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig, use_container_width=True)

    # --- 수치 비교 테이블 ---
    st.markdown("#### 📋 수치 비교")
    st.dataframe(compare_df[["App"] + available_features], use_container_width=True)

else:
    st.info("👈 왼쪽에서 비교할 게임을 1개 이상 선택하세요.")
