import streamlit as st



st.set_page_config(page_title='Sync', page_icon= '🤝')

st.markdown("# 🤝모두의 점심 데이터 비교 합치기🤝")
st.sidebar.header("모두의 점심 데이터 비교 합치기")

if st.button("데이터 동기화 하기"):
    # API 목록 갖고오고
    # 그중 내것을 배고
    # 목록을 순회 하면서 나의 df 랑 비교해서 없는 것 => 데이터프레임으로 만들고
    # 데이터 프로엠을 순회 하면서 insert 한다
    st.success(f"잔업 완료 - 새로운 원천 00 곳에서 총 00 건을 새로 추가하였습니다.")