import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection , get_popular_menu


st.subheader("Top Popular Menu")
st.markdown('''![img](https://mblogthumb-phinf.pstatic.net/20160408_146/what654_14601204776259k2jJ_JPEG/attachImage_3392821268.jpeg?type=w800)''')
# 예시: DataFrame을 불러온 후 메뉴별 빈도 계산
df = pd.read_csv('note/menu.csv') 


popular_menu_df = get_popular_menu()

if popular_menu_df is not None and not popular_menu_df.empty:
    st.dataframe(popular_menu_df)
else:
    st.warning("데이터를 가져오는 데 실패했습니다. 다시 시도해주세요.")
