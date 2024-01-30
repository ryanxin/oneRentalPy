import streamlit as st
import pandas as pd
import numpy as np


# 创建数据库引擎
# engine = create_engine('mysql+pymysql://user:password@host/dbname')

# 查询数据库
# with engine.connect() as conn:
#     result = conn.execute("SELECT * FROM your_table")
#     rows = result.fetchall()

# Re-reading the file to process multi-line orders correctly
# Orders are identified by a unique order number, but their items span multiple rows until a new order number appears.

# Helper function to process each sheet
def process_orders(sheet):
    # Empty list to collect all orders data
    orders_data = []
    # Temporary dictionary to store current order data
    current_order = {}
    # Iterate over each row in the sheet
    for _, row in sheet.iterrows():
        # Check if the row has a new order number; if so, reset current order
        if pd.notna(row['订单号']) and row['订单号'] != current_order.get('订单号'):
            if current_order:
                # If there is a current order being processed, append it to the orders data list
                orders_data.append(current_order)
            current_order = {'订单号': row['订单号'], 'items': [], '订单状态': row['订单状态']}
        # If the order status is paid and the product name and quantity are not NaN, add the item to the current order
        if pd.notna(row['商品名称']) and pd.notna(row['数量']) and current_order.get('订单状态') == '已支付':
            current_order['items'].append((row['商品名称'], row['数量']))
    # Append the last order after finishing the loop
    if current_order:
        orders_data.append(current_order)
    return orders_data

# Process each sheet and combine the data into a single list
all_orders_data = []



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
        stats = process_orders(df)
        
        # 将单个文件的统计数据添加到列表中
        all_stats.append(stats)
    # 将所有统计数据转换为DataFrame
    summary_stats_df = pd.DataFrame(all_stats)