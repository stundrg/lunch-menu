import streamlit as st
from lunch_menu.db import insert_menu, get_connection

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

# 오늘 점심 안한 사람을 알 수 있는 버튼 만들자

st.subheader("범인색출")

c_press = st.button("누구냐 너... 밥 만 홀랑 먹고 입력 안한 너...")
query = """
SELECT
    m.name,
    COUNT(l.id) AS cnt
FROM
    member m
    LEFT JOIN lunch_menu l
ON l.member_id = m.id
    AND l.dt = CURRENT_DATE
GROUP BY
    m.id, m.name
HAVING
    COUNT(l.id) = 0
ORDER BY
    m.name ASC;
"""
if c_press:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            st.write("모두 입력 했습니다.")
        else:
            names = [row[0] for row in rows]
            name_str = ", ".join(names)
            count = len(names)
            st.success(f"범인은?!: {name_str} 입니다. 총{count}명 입니다.")
    except Exception as e:
        st.warning("조회 중 오류가 발생했지비..")
        print(f"Exception: {e}")
