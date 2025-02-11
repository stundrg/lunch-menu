import streamlit as st
import pandas as pd
from lunch_menu.db import get_connection, insert_data, select_table

st.subheader("Noodle Bulk Insert")
Noodle_press = st.button("라면 한방에 인서트")

if Noodle_press:
    try:
        df = pd.read_csv('note/Noodle.csv')

        columns = ['date', 'company','food_name','price']
    # 결과를 담을 리스트를 생성
        results = []
        fail_count = 0

    # 각 행에 대해 insert 실행
        for _, row in df.iterrows():
            try:
                success = insert_data('ramen_data',columns, row['date'], row ['company'], row['food_name'],row['price'])
                results.append(success)
            except Exception as e:
                results.append(False)
                fail_count += 1
                print(f"[Error] Error inserting row: {row.to_dict()} -> Error : {e}")

        # 3. 성공/실패에 따라 메시지 출력
        total_count = len(results)
        true_count = total_count - fail_count

        if fail_count == 0:
            st.success(f"Noodle Bulk insert Success!!! 총{total_count}건 중 {true_count}건 성공")
        else:
            st.error(f"Noodle Bulk insert Fail!! 총{total_count}건 중 {fail_count} 건 실패 ")
    except Exception as e:
        st.warning("Bulk Noodle insert Error")
        print(f"Exception: {e}")
