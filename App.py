import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from lunch_menu.db import get_connection, db_name, insert_menu, select_table

members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

st.title(f"현룡 점심 기록장{db_name}")
st.subheader("입력")



st.subheader("확인")

select_df = select_table()

select_df



st.write("""
##  소크라테스는 말했다.

## '오늘 점심 뭐먹지?'

![img](https://cdnweb01.wikitree.co.kr/webdata/editor/201608/14/img_20160814095841_398f23f1.jpg)
""" )


