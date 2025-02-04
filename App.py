import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("순심 팀 점심 기록장")
st.subheader("입력")
menu = st.text_input("오늘 점심", placeholder = "예 : 김치찌개")
member_name = st.text_input("내 이름", placeholder = "예: 강현룡", value = "hyun")
dt = st.date_input("YUMMY DATE")







st.write("""
# ~ 야무지게 먹어야징 ~

         배고프다...

![img](https://cdnweb01.wikitree.co.kr/webdata/editor/201608/14/img_20160814095841_398f23f1.jpg)
""" )

df = pd.read_csv('note/menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'],
value_vars=df.columns[start_idx:-2],
                        var_name='dt',value_name = 'menu')

not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
#gdf.plot(x='ename', y='menu'. kind = 'bar'

gdf

# 📊 Matplotlib로 바 차트 그리기

fig, ax = plt.subplots()
gdf.plot(x='ename',y = 'menu', kind = 'bar', ax=ax)
st.pyplot(fig)
