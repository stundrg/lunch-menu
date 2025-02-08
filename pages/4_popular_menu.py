import pandas as pd
import matplotlib.pyplot as plt
#from lunch_menu.db import 


# 예시: DataFrame을 불러온 후 메뉴별 빈도 계산
df = pd.read_csv('note/menu.csv') 

# 메뉴별 빈도 계산
menu_count = df['menu_name'].value_counts()
