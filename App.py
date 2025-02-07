import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv
from lunch_menu.db import get_connection

members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}
# https://docs.streamlit.io/develop/concepts/connections/secrets-management
load_dotenv()
db_name = os.getenv("DB_NAME")

DB_CONFIG = {
    "user" : os.getenv("DB_USERNAME"),
    "dbname" : db_name,
    "password" : os.getenv("DB_PASSWORD"),
    "host" : os.getenv("DB_HOST"),
    "port" : os.getenv("DB_PORT")
}
def insert_menu(menu_name, member_id, dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                """INSERT INTO lunch_menu (menu_name, member_id, dt) VALUES (%s, %s, %s);""",
                (menu_name, member_id, dt)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Exception:{e}")
        return False
df = pd.read_csv('note/menu.csv')
st.title(f"현룡 점심 기록장{db_name}")
st.subheader("입력")
menu_name = st.text_input("오늘 점심", placeholder = "예 : 김치찌개")
# member_name = st.text_input("먹은 사람", value = "hyun")
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
# HOMEWORK
# 오늘 점심 안한 사람을 알 수 있는 버튼 만들자

st.subheader("범인색출")
c_press = st.button("누구냐 너... 밥 만 홀랑 먹고 입력 안한 너...")
#query = """
#SELECT
#	l.menu_name,
#	m.name,
#	l.dt
#FROM 
#	lunch_menu l  
#	inner join member m
#	on l.member_id = m.id
#	;
#"""
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

st.subheader("확인")
query = """
SELECT
	l.menu_name,
	m.name,
	l.dt
FROM
	lunch_menu l
	inner join member m
	on l.member_id = m.id
	;
"""
conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()

# selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns = ['a','b','c'])
select_df = pd.DataFrame(rows, columns = ['menu','ename','dt'])
select_df



st.write("""
##  소크라테스는 말했다.

## '오늘 점심 뭐먹지?'

![img](https://cdnweb01.wikitree.co.kr/webdata/editor/201608/14/img_20160814095841_398f23f1.jpg)
""" )


st.subheader("통계")
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
try:
    fig, ax = plt.subplots()
    gdf.plot(x='ename',y='menu', kind='bar', ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}" )

# TODO
# CSV 로드 한번에 다 디비에 INSERT 하는거 하지만 실패 되면 실패한 값 보여주는 거
st.subheader("Bulk Insert")
ggoock_press = st.button("한방에 인서트")
if ggoock_press:
    try:
        df = pd.read_csv('note/menu.csv')
        start_idx = df.columns.get_loc('2025-01-07')
        melted_df = df.melt(id_vars=['ename'] ,value_vars=df.columns[start_idx:-2],
                         var_name='dt',value_name = 'menu')

        not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
    # 1. 결과를 담을 리스트를 생성
        results = []
    # 각 행에 대해 insert 실행
        for _, row in not_na_df.iterrows():
            m_id = members[row['ename']]
            try:
                insert_menu(row['menu'], m_id, row['dt'])
                results.append(True)
            except Exception as e:
                results.append(False)
                print(f"Error inserting row: {row}, Error : {e}")

        # 3. 성공/실패에 따라 메시지 출력
            total_count = len(results)
            true_count = sum(results)
            false_count = total_count - true_count
        
            if false_count == 0:
                st.success(f"Bulk insert Success 총{total_count}건 중 {true_count}건 성공")
            else:
                st.error(f"Bulk insert Fail 총{total_count}건 중 {false_count}건 실패")
    except Exception as e:
        st.warning("Bulk insert Error")
        print(f"Exception: {e}")
