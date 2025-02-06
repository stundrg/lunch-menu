import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv

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

def get_connection():
    return psycopg.connect(**DB_CONFIG)

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

st.subheader("확인")
query = """SELECT menu_name AS menu, member_id as ename, dt  FROM lunch_menu ORDER BY dt desc"""
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

# 📊 Matplotlib로 바 차트 그리기
try:
    fig, ax = plt.subplots()
    gdf.plot(x='ename',y='menu', kind='bar', ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}" )

# TODO
# CSV 로드 한번에 다 디비에 INSERT 하는거
st.subheader("Bulk Insert")
if st.button("한방에 인서트"):
    df = pd.read_csv('note/menu.csv')
    start_idx = df.columns.get_loc('2025-01-07')
    melted_df = df.melt(id_vars=['ename'] ,value_vars=df.columns[start_idx:-2],
                         var_name='dt',value_name = 'menu')

    not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
    for _, row in not_na_df.iterrows():
        insert_menu(row['menu'], row['ename'], row['dt'])

    st.success(f"벌크 인서트 성공")

