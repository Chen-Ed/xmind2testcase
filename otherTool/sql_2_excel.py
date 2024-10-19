# 遍历文件夹下的sql文件，提取创表的约束信息，转换为excel表格


import re
import pandas as pd
from datetime import datetime
import os


def parse_sql_create_table(sql):
    # 使用正则表达式匹配字段信息
    pattern = r'`(\w+)`\s+(\S+)\s+(.+?)\sCOMMENT\s+\'(.+?)\'*,'
    matches = re.findall(pattern, sql)

    columns = []
    for match in matches:
        column = {
            '字段名': match[0],
            '类型': match[1],
            '约束条件': match[2],
            '字段注释': match[3]
        }
        columns.append(column)

    return columns


def extract_constraints(constraint_str):
    constraints = []
    if 'NOT NULL' in constraint_str:
        constraints.append('NOT NULL')
    if 'AUTO_INCREMENT' in constraint_str:
        constraints.append('AUTO_INCREMENT')
    if 'DEFAULT' in constraint_str:
        default_value = re.search(r"DEFAULT\s+['\"]?([^'\"]+)", constraint_str)
        if default_value:
            constraints.append(f'DEFAULT {default_value.group(1)}')
    return ', '.join(constraints)


def save_to_excel(df, filename):
    # 获取当前用户的桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    file_path = os.path.join(desktop_path, filename)

    # 保存文件
    df.to_excel(file_path, index=False)
    print(f"Excel file saved to: {file_path}")


def main(sql:str):
    # 提取表名
    table_name_pattern = r'CREATE\s+TABLE\s+`?(\w+)`?\s+\('
    table_name_match = re.search(table_name_pattern, sql)
    if table_name_match:
        table_name = table_name_match.group(1)
    else:
        raise ValueError("Table name not found.")

    # 找到 CREATE TABLE 语句
    create_table_pattern = r'CREATE\s+TABLE\s+.+?\s*\((.+)\)\s*ENGINE\s+=\s+InnoDB.*?ROW_FORMAT.*?;'
    create_table_match = re.search(create_table_pattern, sql, re.DOTALL)

    if create_table_match:
        key_sql = create_table_match.group(1).strip()

        # 解析 SQL 语句
        columns = parse_sql_create_table(key_sql)

        # 提取约束条件
        for column in columns:
            column['约束条件'] = extract_constraints(column['约束条件'])

        # 构建 DataFrame
        df = pd.DataFrame(columns)
        df['默认值'] = df['约束条件'].apply(lambda x: x.split(' ')[-1] if 'DEFAULT' in x else '')
        df['约束条件'] = df['约束条件'].apply(lambda x: x.replace(f'DEFAULT {df.loc[df.index, "默认值"]}', '').strip())

        # 添加表名和注释字段
        df['表名'] = table_name

        return df



if __name__ == "__main__":
    index = 0
    df = None
    for root,dirs,files in os.walk(r'C:\Users\te_chenyingdong\Desktop\数据组件1.77-校验'):
        for file in files:
            if file.endswith('.sql'):
                print('处理文件：'+file)
                with open(os.path.join(root,file),'r',encoding='utf-8') as f:
                    sql = f.read()
                    if index == 0:
                        df = main(sql)
                    else:
                        df = pd.concat([df,main(sql)], axis=0, ignore_index=True)
                    index += 1
            else:
                raise ValueError("No SQL file found.")
    # 保存到 Excel
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"table_structure_{timestamp}.xlsx"
    save_to_excel(df, filename)