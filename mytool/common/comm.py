import os

import jsonschema
import requests
from loguru import logger
# from importlib import import_module

# # 获取当前文件所在目录
# ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # 定义项目内各文件夹路径
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

def vailidata_OpenAPI(api: dict,SCHEMA):
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


# 打印路径以确认
if __name__ == "__main__":
    print("ROOT Directory:", ROOT)
    print("ADDONS Directory:", ADDONS)
    print("CACHE Directory:", CACHE)
    print("TEMPLATES Directory:", TEMPLATES)
    print("RUNNER Directory:", RUNNER)
    print("COMMON Directory:", COMMON)
