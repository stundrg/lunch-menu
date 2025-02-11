import streamlit as st
import requests
import datetime
import lunch_menu.constants as const
st.set_page_config(page_title="API", page_icon="🗓")

st.markdown("# 🍽️ API")
st.sidebar.header("나이 계산기")


# 오늘 날짜 가져오기
today = datetime.date.today()

min_date = today.replace(year=today.year - 100)  
max_date = today  


dt = st.date_input("생일 입력" ,min_value=min_date ,max_value=max_date)
if st.button("메뉴 저장"):
    headers = {
        'accept' : 'application/json'
    }
    API_URL = 'https://agecalculator.calcalhan.store/api/py/ageCalculator'
    r = requests.get(f'{const.API_AGE}/{dt}',headers=headers)
    if r.status_code == 200:
        data = r.json()
        age = data['age']
        st.success(f"{dt} 생의 나이는 {age}살 입니다.")
    else:
        st.error(f"문제가 발생하였습니다. 관리자 문의: {r.status_code}")    