import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection


st.subheader("Top Popular Menu")
st.markdown('''![img](https://mblogthumb-phinf.pstatic.net/20160408_146/what654_14601204776259k2jJ_JPEG/attachImage_3392821268.jpeg?type=w800)''')
# 예시: DataFrame을 불러온 후 메뉴별 빈도 계산
df = pd.read_csv('note/menu.csv') 

# 메뉴별 빈도 계산
def get_popular_menu():
    # 인기 메뉴를 찾는 SQL 쿼리
    query = """
    SELECT menu_name, COUNT(*) AS menu_count
    FROM lunch_menu
    GROUP BY menu_name
    ORDER BY menu_count DESC;
    """

    try:
        # 데이터베이스 연결
        conn = get_connection()

        # 쿼리 실행 및 결과를 DataFrame으로 변환
        df = pd.read_sql(query, conn)
        # 연결 종료
        conn.close()

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

# 실행 예시
if __name__ == "__main__":
    popular_menu_df = get_popular_menu()
    if popular_menu_df is not None:
        print(popular_menu_df)
    else:
        print("Failed to retrieve popular menu data.")

popular_menu_df = get_popular_menu()

if popular_menu_df is not None and not popular_menu_df.empty:
    st.dataframe(popular_menu_df)
else:
    st.warning("데이터를 가져오는 데 실패했습니다. 다시 시도해주세요.")
