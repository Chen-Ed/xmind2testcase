# -*- coding: utf-8 -*-
import pathlib
import time
from functools import wraps

from loguru import logger


def csv_2_excel(csv_name: str, excel_name: str, sep=','):
    """
    将csv文件转换为excel文件，并保存为excel_name，默认sheet_name为sheet1，默认分隔符为','。
    :param excel_name: excel文件路径，如'test.xlsx'
    :param csv_name: csv文件路径，如'test.csv'
    :param sep: csv文件分隔符，默认为','
    """
    import openpyxl

    excel_name = pathlib.Path(excel_name)
    csv_name = pathlib.Path(csv_name)

    if not csv_name.exists():
        raise ValueError(f"{csv_name} file not exists!")
    if not csv_name.suffix == '.csv' or not excel_name.suffix == '.xlsx':
        raise ValueError("csv_name or excel_name file suffix error!")

    # opening the files
    wb = openpyxl.load_workbook(excel_name)
    sheet = wb.worksheets[0]

    with open(csv_name, "r", encoding="utf-8") as file:
        # rows and columns
        row = 1
        column = 1

        # for each line in the file
        for line in file:
            # remove the \n from the line and make it a list with the seperator
            line = line[:-1]
            line = line.split(sep)

            # for each data in the line
            for data in line:
                # write the data to the cell
                sheet.cell(row, column).value = data
                # after each data column number increases by 1
                column += 1

            # to write the next line column number is set to 1 and row number is increased by 1
            column = 1
            row += 1

        # saving the excel file and closing the csv file
        wb.save(excel_name)
        logger.info("Csv 2 Excel file successfully")


def csv_2_json(csv_name: str, toWriteJson: bool = False, sep=','):
    """
    将csv文件转换为json，并保存为json文件，默认分隔符为','。
    :param toWriteJson: 是否保存转换的json文件，默认放在csv同一目录下，默认为 False
    :param csv_name: csv文件路径，如'test.csv'
    :param sep: csv文件分隔符，默认为','
    """
    import csv
    import json

    csv_name = pathlib.Path(csv_name)
    json_name = pathlib.Path(csv_name.parent, csv_name.stem + '.json')
    if not csv_name.exists():
        raise ValueError(f"{csv_name} file not exists!")
    if not csv_name.suffix == '.csv':
        raise ValueError("csv_name file suffix error!")

    with open(csv_name, 'r', encoding='utf8') as f:

        reader = csv.reader(f, delimiter=sep)
        titles = []
        temp_data = {}

        for heading in reader:
            titles = heading
            break

        i = 1
        for row in reader:
            current_row = "row{}".format(i)
            temp_data['{}'.format(current_row)] = {}
            for col in range(len(titles)):
                temp_data[current_row][titles[col]] = row[col]
            i += 1
    if toWriteJson:
        with open(json_name, 'w', encoding='utf-8') as f_j:
            json.dump(temp_data, f_j, indent=4, ensure_ascii=False)

    logger.info("File converted successfully :)")
    return temp_data


def excel_2_json(excel_path: str, sheet_name: str = 'Sheet1', toWriteJson: bool = False):
    """
    将Excel文件转换为字典。
    :param excel_path: Excel文件路径
    :param sheet_name: Excel工作表名称，默认为'Sheet1'
    :param toWriteJson: 是否保存转换的json文件，默认放在excel同一目录下，默认为 False
    :return: 包含Excel数据的字典
    """
    import pandas as pd
    import json
    # 检查文件是否存在
    excel_path = pathlib.Path(excel_path)
    if not excel_path.exists():
        raise FileNotFoundError(f"{excel_path} 文件不存在！")
    if excel_path.suffix not in ['.xls', '.xlsx']:
        raise ValueError("excel_path 文件后缀错误！")

    # 读取Excel文件
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # 将DataFrame转换为字典
    data_dict = df.to_dict(orient='records')

    if toWriteJson:
        json_name = pathlib.Path(excel_path.parent, excel_path.stem + '.json')
        with open(json_name, 'w', encoding='utf-8') as f_j:
            json.dump(data_dict, f_j, indent=4, ensure_ascii=False)

    return data_dict


def json_2_csv(json_dict: dict, csv_name: str, sep=','):
    """
    将JSON文件转换为CSV，并保存为CSV文件，默认分隔符为','。
    :param csv_name: CSV文件路径
    :param json_dict: json字典
    :param sep: CSV文件分隔符，默认为','
    """
    import csv

    if pathlib.Path(csv_name).suffix != '.csv' or csv_name is None:
        raise ValueError("csv_name file suffix error!")

    # 获取列标题
    titles = list(json_dict[next(iter(json_dict))].keys())

    # 写入CSV文件
    with open(csv_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=sep)
        writer.writerow(titles)

        for row_key, row_data in json_dict.items():
            row = [row_data.get(title, '') for title in titles]
            writer.writerow(row)

    logger.info("File converted successfully :)")


def json_2_excel(json_dict: dict, excel_name: str):
    """
    将JSON数据转换为Excel文件。
    :param json_dict: JSON数据字典
    :param excel_name: Excel文件路径，默认为'output.xlsx'
    """
    import pandas as pd

    if pathlib.Path(excel_name).suffix not in ['.xls', '.xlsx']:
        raise ValueError("excel_name file suffix error!")

    # 获取列标题
    titles = list(json_dict[next(iter(json_dict))].keys())

    # 创建DataFrame
    df = pd.DataFrame(columns=titles)

    # 添加数据
    for row_key, row_data in json_dict.items():
        row = {title: row_data.get(title, '') for title in titles}
        df = df.append(row, ignore_index=True)

    # 重置索引
    df.reset_index(drop=True, inplace=True)

    # 写入Excel文件
    df.to_excel(excel_name, index=False)

    logger.info("File converted successfully :)")


def json_2_yaml(json_dict: dict, yaml_name: str):
    import yaml

    yaml_name = pathlib.Path(yaml_name)
    if not yaml_name.suffix == '.yaml':
        raise ValueError("json_name file suffix error!")

    # Processing the conversion
    output = yaml.dump(json_dict)

    with open(yaml_name, 'w', encoding='utf8') as y_f:
        y_f.write(output)

    logger.info("File converted successfully :)")

    return output


def retry(tries, delay=3, backoff=2):
    """
    Decorator that retries a function call (with arguments) several times.
    delay sets the initial delay in seconds, and backoff sets the factor by which the delay should lengthen after each failure.
    tries sets the maximum number of attempts.
    """

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logger.error(e)
                    msg = "%s 出错了,  %d 秒后进行重试..." % (str(f.__name__), mdelay)
                    logger.error(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
