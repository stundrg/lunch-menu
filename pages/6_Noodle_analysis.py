import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from lunch_menu.db import get_connection ,get_noodle_count_by_year


# st.markdown('''![img]()''')
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

plt.rcParams['axes.unicode_minus'] = False

try:
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_prop.get_name()
except Exception:
    plt.rcParams["font.family"] = "DejaVu Sans"  # 한글 폰트 없을 경우 기본 폰트

# 음수 기호 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False

df = get_noodle_count_by_year()

st.markdown("## 연도 별 출시 라면 수")

if df is not None and not df.empty:
   
    # 그래프 출력
    fig, ax = plt.subplots()
    ax.bar(df["date"], df["ramen_count"], color="orange")
    ax.set_xlabel("출시 연도")
    ax.set_ylabel("출시된 라면 수")
    ax.set_title("연도별 출시 라면 개수")
    st.pyplot(fig)
else:
    st.warning("데이터를 가져올 수 없습니다.")


# 표 출력
st.dataframe(df)


