import streamlit as st
import pandas as pd
import altair as alt

# CSV 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

st.title("🌍 MBTI 유형별 국가 분포 Top 10")

# MBTI 유형 리스트
types = [col for col in df.columns if col != "Country"]

# 선택 박스에서 MBTI 유형 선택
selected_type = st.selectbox("MBTI 유형을 선택하세요:", types)

# Top 10 국가 추출
top10 = df[["Country", selected_type]].sort_values(by=selected_type, ascending=False).head(10)

st.write(f"### {selected_type} 유형 비율이 가장 높은 국가 Top 10")

# Altair 그래프 생성
chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(selected_type, title="비율", scale=alt.Scale(domain=[0, top10[selected_type].max()*1.1])),
        y=alt.Y("Country", sort="-x", title="국가"),
        tooltip=["Country", selected_type]
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)
