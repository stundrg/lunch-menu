import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg

DB_CONFIG = {
    "dbname" : "sunsindb",
    "user" : "sunsin",
    "password" : "mysecretpassword",
    "host" : "localhost",
    "port" : "5432"
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

st.title("현룡 점심 기록장")
st.subheader("입력")
menu_name = st.text_input("오늘 점심", placeholder = "예 : 김치찌개")
member_name = st.text_input("나의 이름", placeholder = "예: 강현룡", value = "hyun")
dt = st.date_input("YUMMY DATE")
isPress = st.button("메뉴 저장")

if isPress:
    if menu_name and member_name and dt:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lunch_menu (menu_name, member_name, dt) VALUES (%s, %s, %s);",
            (menu_name, member_name, dt)
        )
        conn.commit()
        cursor.close()
        st.success(f"버튼{isPress} // {menu_name} // {member_name} // {dt}")
    else:
        st.warning(f"모든 값을 입력해주세요!")

st.subheader("확인")
query = """SELECT menu_name, member_name, dt FROM lunch_menu ORDER BY dt desc"""

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

# conn.commit()
cursor.close()


# selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns = ['a','b','c'])
select_df = pd.DataFrame(rows, columns = ['menu','ename','dt'])
select_df



st.write("""
##  소크라테스는 말했다.

## '오늘 점심 뭐먹지?'

![img](https://cdnweb01.wikitree.co.kr/webdata/editor/201608/14/img_20160814095841_398f23f1.jpg)
""" )

#해당 코드는 제가 만든 코드로 상관없는코드입니다
#st.subheader("통계")
#df = pd.read_csv('note/menu.csv')


#start_idx = df.columns.get_loc('2025-01-07')

#melted_df = df.melt(id_vars=['ename'],
#                    value_vars=df.columns[start_idx:-2],
#                    var_name='dt', value_name='menu')

#not_na_df = melted_df[~melted_df['menu'].isin(['-', 'x', '<결석>'])]

#gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
#hyun_count = gdf.loc[gdf['ename'] == 'hyun', 'menu'].values[0] if 'hyun' in gdf['ename'].values else 0
#gdf
#st.write(f"Hyun이 먹은 메뉴 개수: {hyun_count}")


st.subheader("통계")
df = pd.read_csv('note/menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'],
value_vars=df.columns[start_idx:-2],
                        var_name='dt',value_name = 'menu')

not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
#gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
gdf = select_df.groupby('ename')['menu'].count().reset_index()
#gdf.plot(x='ename', y='menu'. kind = 'bar')

gdf

# 📊 Matplotlib로 바 차트 그리기

fig, ax = plt.subplots()
gdf.plot(x='ename',y = 'menu', kind = 'bar', ax=ax)
st.pyplot(fig)
# TODO
# CSV 로드 한번에 다 디비에 INSERT 하는거
st.subheader("Bulk Insert")
if st.button("한방에 인서트"):
    conn = get_connection()
    cursor = conn.cursor()

    insert_df = df[['menu', 'ename', 'date']].rename(columns={'menu_name' : 'menu', 'member_name': 'ename', 'dt':'date'})
    cursor.executemany(
            "INSERT INTO lunch_menu (menu_name, member_name, dt) VALUES (%s, %s, %s)",
        df[['menu_name', 'member_name', 'dt']].values.tolist()
    )
    conn.commit()
    cursor.close()
    st.success(f"{len(df)}개의 데이터 추가 완료!")


