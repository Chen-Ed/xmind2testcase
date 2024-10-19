import os

import jsonschema
import requests
from loguru import logger
import pathlib
import time
from functools import wraps

# from importlib import import_module

# # 获取当前文件所在目录
HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
# 定义项目内各文件夹路径
DOCS = ROOT / 'docs'
MYTOOL = ROOT / 'mytool'
OTHERTOOL = ROOT / 'otherTool'
WEBTOOL = ROOT / 'webtool'
XMIND2TESTCASE = ROOT / 'xmind2case'


# ADDONS = os.path.join(ROOT, 'addons')
# CACHE = os.path.join(ROOT, 'cache')
# TEMPLATES = os.path.join(ROOT, 'pycodeTemplates')
# RUNNER = os.path.join(ROOT, 'runner')
# COMMON = os.path.join(ROOT, 'common')


def check_status_code(response: requests.Response, log: logger) -> None:
    """
    检查请求响应状态码是否为200，并根据结果使用logger记录信息。

    :param response: requests.Response 对象
    :param log: logging.Logger 对象
    """

    try:
        if response.status_code == 200 and response.json()['code'] == 200:
            log.info("请求成功，两种状态码均：200")
        else:
            log.warning(f"请求失败，接口状态码：{response.status_code}")
            log.warning(f"预期返回 系统内部状态码200，实际收到：{response.json()['code']}")
    except Exception as e:
        log.error(e)


# def check_status_code(response: requests.Response, logger) -> None:
#     """
#     检查请求响应状态码是否为200，并根据结果使用logger记录信息。
#
#     :param response: requests.Response 对象
#     :param log: logging.Logger 对象
#     """
#
#     assert response.status_code == 200, f"请求失败，接口状态码：{response.status_code}"
#     assert response.json().get('code') == 200, f"预期返回 系统内部状态码200，实际收到：{response.json().get('code')}"


def vailidata_OpenAPI(api: dict, SCHEMA):
    """
    验证OpenAPI/Har文件是否合法，并返回结果。

    :param SCHEMA: OpenAPI/Har 校验格式
    :return: 通过True ，不通过False
    """

    # 执行验证
    try:
        jsonschema.validate(api, SCHEMA)
        logger.info("SCHEMA验证通过")
        return True
    except jsonschema.exceptions.ValidationError as e:
        logger.warning(f"验证失败: {e.message}")
        return e


def csv_2_excel(csv_path, excel_path, sep=',', encoding='utf-8'):
    """
    将csv文件转换为excel文件，并保存为excel_name，默认sheet_name为sheet1，默认分隔符为','。
    :param excel_path: excel文件路径，如'test.xlsx'
    :param csv_path: csv文件路径，如'test.csv'
    :param sep: csv文件分隔符，默认为','
    """
    import pandas as pd

    excel_path = pathlib.Path(excel_path)
    csv_path = pathlib.Path(csv_path)

    if not csv_path.exists():
        raise ValueError(f"{csv_path} file not exists!")
    if not csv_path.suffix == '.csv' or not excel_path.suffix == '.xlsx':
        raise ValueError("csv_name or excel_name file suffix error!")

    # 读取 CSV 文件
    df = pd.read_csv(csv_path, encoding=encoding)

    # 保存为 Excel 文件
    df.to_excel(excel_path, index=False)
    logger.info(f"Csv 2 Excel file successfully {excel_path}")


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


# 打印路径以确认
if __name__ == "__main__":
    print("ROOT Directory:", ROOT)
    # print("ADDONS Directory:", ADDONS)
    # print("CACHE Directory:", CACHE)
    # print("TEMPLATES Directory:", TEMPLATES)
    # print("RUNNER Directory:", RUNNER)
    # print("COMMON Directory:", COMMON)
