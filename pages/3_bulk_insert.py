import streamlit as st
import pandas as pd
from lunch_menu.db import get_connection, db_name, insert_menu, select_table


members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

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
        fail_count = 0
        false_count =-
    # 각 행에 대해 insert 실행
        for _, row in not_na_df.iterrows():
            m_id = members[row['ename']]
            if m_id is None:
                results.append(False)
                fail_count += 1
                print(f"[EEROR] Unknown member : {row['ename']}")
                # failed_rows.append(f"Unknown member: {row['ename']}")
                continue

            try:
                insert_menu(row['menu'], m_id, row['dt'])
                results.append(True)
            except Exception as e:
                results.append(False)
                print(f"[Error] Error inserting row: {row.to_dict()} -> Error : {e}")

        # 3. 성공/실패에 따라 메시지 출력
        total_count = len(results)
        true_count = sum(results)

        if fail_count == 0:
            st.success(f"Bulk insert Success 총{total_count}건 중 {true_count}건 성공")
        else:
            st.error(f"Bulk insert Fail 총{total_count}건 중 {false_count}건 실패")
    except Exception as e:
        st.warning("Bulk insert Error")
        print(f"Exception: {e}")
