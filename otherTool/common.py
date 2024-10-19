import requests


def check_status_code(response: requests.Response, logger) -> None:
    """
    检查请求响应状态码是否为200，并根据结果使用logger记录信息。

    :param response: requests.Response 对象
    :param log: logging.Logger 对象
    """

    assert response.status_code == 200, f"请求失败，接口状态码：{response.status_code}"
    assert response.json().get('code') == 200, f"预期返回 系统内部状态码200，实际收到：{response.json().get('code')}"
