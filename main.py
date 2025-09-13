import streamlit as st
import pandas as pd
import altair as alt
import os

# ----------------------
# 기본 설정
# ----------------------
st.set_page_config(page_title="MBTI 국가별 비율 Top10", page_icon="🌍", layout="centered")

st.title("🌍 MBTI 유형별 국가 Top 10 비율 시각화")
st.write("CSV 파일을 기본적으로 같은 폴더에서 불러옵니다. 만약 해당 파일이 없으면 업로드한 CSV 파일을 사용합니다.")

# ----------------------
# CSV 불러오기 (기본: 로컬, 예외: 업로드)
# ----------------------
def load_data():
    default_path = "countriesMBTI_16types"  # 같은 폴더에 있다고 가정
    if os.path.exists(default_path):
        st.info(f"기본 데이터 파일 `{default_path}` 를 불러왔습니다.")
        return pd.read_csv(default_path)
    else:
        uploaded_file = st.file_uploader("📂 CSV 파일 업로드", type=["csv"])
        if uploaded_file:
            st.info("업로드한 CSV 파일을 사용합니다.")
            return pd.read_csv(uploaded_file)
        else:
            return None

# 데이터 불러오기
df = load_data()

if df is not None:
    # 컬럼 확인
    st.write("데이터 미리보기:")
    st.dataframe(df.head())

    # MBTI 유형 선택
    mbti_list = sorted(df["MBTI"].unique())
    mbti_choice = st.selectbox("👉 MBTI 유형을 선택하세요:", options=mbti_list)

    if mbti_choice:
        # 선택한 MBTI 필터링
        filtered = df[df["MBTI"] == mbti_choice]

        # 비율 높은 순으로 정렬 후 Top 10 추출
        top10 = filtered.sort_values("Percentage", ascending=False).head(10)

        # ----------------------
        # Altair 그래프
        # ----------------------
        chart = (
            alt.Chart(top10)
            .mark_bar()
            .encode(
                x=alt.X("Percentage:Q", title="비율(%)"),
                y=alt.Y("Country:N", sort="-x", title="국가"),
                tooltip=["Country", "Percentage"]
            )
            .properties(width=600, height=400, title=f"{mbti_choice} 유형 비율 Top 10 국가")
            .interactive()
        )

        st.altair_chart(chart, use_container_width=True)
else:
    st.warning("기본 데이터 파일이 없으며 업로드한 CSV 파일도 없습니다.")
