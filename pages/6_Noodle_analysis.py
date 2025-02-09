import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection ,get_noodle_count_by_year


st.markdown("## 연도 별 출시 라면 수")
# st.markdown('''![img]()''')
df = get_noodle_count_by_year()

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


