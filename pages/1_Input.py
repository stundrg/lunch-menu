import streamlit as st
from lunch_menu.db import insert_menu

st.set_page_config(page_title="Input", page_icon="💻")

st.markdown("# ヾ(≧▽≦*)o INPUT Menu")
st.sidebar.header("INPUT Menu")

## TODO = 메뉴 입력하기 부분 코드 이동 시키기 
members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

menu_name = st.text_input("오늘 점심", placeholder = "예 : 김치찌개")
member_name = st.selectbox(
        "먹은 사람",
        options = list(members.keys()),
        index = list(members.keys()).index('hyun') # index 값으로 디폴트 값 지정 가능
    )
member_id = members[member_name]

dt = st.date_input("YUMMY DATE")

isPress = st.button("메뉴 저장")

if isPress:
    # member_name 을 member_id로 바꾸어서 DB에 id 가 insert 되도록 하기
    if menu_name and member_id and dt:
        if insert_menu(menu_name, member_id, dt):
            st.success(f"입력 성공")
        else:
            st.error(f"입력 실패")
    else:
        st.warning(f"모든 값을 입력해주세요!")
