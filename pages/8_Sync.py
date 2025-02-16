import streamlit as st
import requests
import lunch_menu.constants as const
import datetime
import pandas as pd
from lunch_menu.db import select_table_sync, insert_menu, get_connection

st.set_page_config(page_title='Sync', page_icon= '🤝')

st.markdown("# 🤝모두의 점심 데이터 비교 합치기🤝")
st.sidebar.header("모두의 점심 데이터 비교 합치기")

API_URL = "https://raw.githubusercontent.com/stundrg/lunch-menu/refs/heads/main/endpoints.json"

API_URL = "https://raw.githubusercontent.com/stundrg/lunch-menu/refs/heads/main/endpoints.json"

# 🔹 API에서 데이터 가져오기
def fetch_external_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())  # JSON 데이터를 DataFrame으로 변환
    else:
        st.error("❌ 데이터 불러오기 실패")
        return None

# 🔹 동기화 실행
if st.button("데이터 동기화 하기"):
    df_external = fetch_external_data()  # 외부 데이터 가져오기
    if df_external is None:
        st.stop()

    df_local = select_table_sync()  # 기존 데이터 가져오기

    if df_local.empty:
        new_data = df_external  # 기존 데이터가 없으면 전부 추가
    else:
        # 🔹 중복 제거 (menu_name, name, dt 비교)
        query = """
        SELECT df_external.menu_name, df_external.name, df_external.dt
        FROM df_external 
        LEFT JOIN df_local 
        ON df_external.dt = df_local.dt 
        AND df_external.name = df_local.name 
        AND df_external.menu_name = df_local.menu_name
        WHERE df_local.menu_name IS NULL
        """
        pysqldf = lambda q: sqldf(q, globals())
        new_data = pysqldf(query)  # 기존 데이터와 비교하여 새로운 데이터만 가져옴

    if new_data.empty:
        st.info("📌 추가할 새로운 데이터가 없습니다.")
        st.stop()

    # 🔹 DB에 새로운 데이터 추가
    members = {
        "TOM": 1, "cho": 2, "hyun": 3, "JERRY": 4, "SEO": 5, "jiwon": 6,
        "jacob": 7, "heejin": 8, "lucas": 9, "nuni": 10, "CHO": 2, "HYUN": 3,
        "JIWON": 6, "JACOB": 7, "HEEJIN": 8, "LUCAS": 9, "NUNI": 10
    }
    
    added_count = 0
    for _, row in new_data.iterrows():
        if row["name"] in members:
            member_id = members[row["name"]]

            # 🔹 중복 확인 후 최종 추가
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT COUNT(*) FROM lunch_menu 
                   WHERE menu_name = %s AND member_id = %s AND dt = %s""",
                (row["menu_name"], member_id, row["dt"])
            )
            if cursor.fetchone()[0] == 0:  # 중복이 없으면 추가
                insert_menu(row["menu_name"], member_id, row["dt"])
                added_count += 1
            cursor.close()
            conn.close()

    st.success(f"✅ 작업 완료 - 총 {added_count} 건의 새로운 데이터를 추가했습니다!")
