import streamlit as st

st.set_page_config(page_title="API", page_icon="🗓")

st.markdown("# 🍽️ API")
st.sidebar.header("나이 계산기")

dt = st.date_input("생일 입력")
if st.button("메뉴 저장"):
    st.success(f"나이 계산{dt}")