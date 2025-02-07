import matplotlib.pyplot as plt
import streamlit as st
from lunch_menu.db import get_connection, db_name, insert_menu, select_table

st.subheader("통계")
select_df = select_table()
gdf = select_df.groupby('ename')['menu'].count().reset_index()
gdf
query ='''
select
    l.menu_name,
    m.name,
    l.dt
from
    member m left join lunch_menu l
on l.dt = Current_date
where l.dt is null;
'''
conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()
# 📊 Matplotlib로 바 차트 그리기

st.subheader("차트")
try:
    fig, ax = plt.subplots()
    gdf.plot(x='ename',y='menu', kind='bar', ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}" )
