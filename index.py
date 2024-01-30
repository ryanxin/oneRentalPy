import streamlit as st
import pandas as pd
import numpy as np
# from sqlalchemy import create_engine
# from index import create_connection
# import mysql.connector
# import pymysql


# 创建数据库引擎
# engine = create_engine('mysql+pymysql://user:password@host/dbname')

# 查询数据库
# with engine.connect() as conn:
#     result = conn.execute("SELECT * FROM your_table")
#     rows = result.fetchall()

#查询数据库
# connection = create_connection("localhost", "root", "password", "database_name")
# def create_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password,
#             database=db_name
#         )
#         print("Connection to MySQL DB successful")
#     except Exception as e:
#         print(f"The error '{e}' occurred")
#     return connection
 
def process_data(df):
    # 数据清洗和转换
    df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)
    df['TotFlArea'] = df['TotFlArea'].replace(',', '', regex=True).astype(float)
    
    # 计算统计数据
    br_0_1 = df[(df['Tot BR'] == 0) | (df['Tot BR'] == 1)]
    br_2 = df[df['Tot BR'] == 2]
    br_3_more = df[df['Tot BR'] >= 3]
    total_avg_price_area = df['Price'].sum() / df['TotFlArea'].sum().astype(float)
    
    stats = {
      'File': df.name,  # 假设你的DataFrame有一个'name'列来标识文件名
      '0 or 1 BR': len(br_0_1),
      '2 BR': len(br_2),
      '3+ BR': len(br_3_more),
      'Total Listings': len(df),
      'Avg Price/Area 0 or 1 BR': round(br_0_1['Price'].sum() / br_0_1['TotFlArea'].sum()) if len(br_0_1) > 0 else 0,
      'Avg Price/Area 2 BR': round(br_2['Price'].sum() / br_2['TotFlArea'].sum()) if len(br_2) > 0 else 0,
      'Avg Price/Area 3+ BR': round(br_3_more['Price'].sum() / br_3_more['TotFlArea'].sum()) if len(br_3_more) > 0 else 0,
      'Total Avg Price/Area': round(total_avg_price_area)
    }
    
    return stats

# Streamlit应用的标题
st.title('房源数据统计')
st.write('上传CSV文件，统计房源数据')


# 文件上传器，允许上传多个文件
uploaded_files = st.file_uploader("选择CSV文件", type="csv", accept_multiple_files=True)
all_stats = []  # 用于存储所有文件的统计数据

if uploaded_files:
    for uploaded_file in uploaded_files:
        # 读取CSV文件到DataFrame
        df = pd.read_csv(uploaded_file)
        df.name = uploaded_file.name  # 将文件名添加到DataFrame
        
        # 处理数据
        stats = process_data(df)
        
        # 将单个文件的统计数据添加到列表中
        all_stats.append(stats)
    # 将所有统计数据转换为DataFrame
    summary_stats_df = pd.DataFrame(all_stats)

    # 显示统计数据表格
    st.table(summary_stats_df)
