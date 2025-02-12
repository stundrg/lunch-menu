import streamlit as st
import requests
import lunch_menu.constants as const
import datetime
import pandas as pd


st.set_page_config(page_title='Sync', page_icon= '🤝')

st.markdown("# 🤝모두의 점심 데이터 비교 합치기🤝")
st.sidebar.header("모두의 점심 데이터 비교 합치기")

API_URL = "https://raw.githubusercontent.com/stundrg/lunch-menu/refs/heads/main/endpoints.json"

if st.button("데이터 동기화 하기"):
# (1) API에서 데이터 목록 가져오기
    response = requests.get(API_URL)
    if response.status_code == 200:
        data_list = response.json()  # JSON 응답을 DataFrame으로 변환
        df_all = pd.DataFrame(data_list)
    else:
        st.error("데이터를 불러오는데 실패했습니다.")
        st.stop()
    # 그 중 내것을 빼고
    # 목록을 순회 하면서 나의 df 랑 비교해서 없는 것 => 데이터프레임으로 만들고
    # 데이터 프로엠을 순회 하면서 insert 한다
    st.success(f"잔업 완료 - 새로운 원천 00 곳에서 총 00 건을 새로 추가하였습니다.")
    
    