import psycopg
import os
from dotenv import load_dotenv
import pandas as pd

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

df = pd.read_csv('note/menu.csv')
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

def select_table():
    query = """
    SELECT
        l.menu_name,
        m.name,
        l.dt
    FROM
        lunch_menu l
    inner join
            member m
    on 
            l.member_id = m.id
    ;
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns = ['menu','ename','dt'])
    return df


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

