# -*- coding: utf-8 -*-

import pymysql
def execute_sql_file(sql_text: str):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='baohui_test',
        charset='utf8mb4'
    )
    try:
        with conn.cursor() as cursor:
            # 分号拆分执行多条语句
            statements = [stmt.strip() for stmt in sql_text.split(';') if stmt.strip()]
            for statement in statements:
                cursor.execute(statement + ';')
        conn.commit()
        print("所有表创建成功！")
    finally:
        conn.close()

# with open('baohui.sql', 'r', encoding='utf-8') as f:
#      sql_text = f.read()

with open('baohui.sql', 'r', encoding='gbk') as f:
    sql_text = f.read()


execute_sql_file(sql_text)
