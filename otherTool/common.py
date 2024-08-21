import time
from functools import wraps
import requests
from loguru import logger


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
                    print(str(e))
                    msg = "%s 出错了,  %d 秒后进行重试..." % (str(f.__name__), mdelay)
                    print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def check_status_code(response: requests.Response,logger) -> None:
    """
    检查请求响应状态码是否为200，并根据结果使用logger记录信息。

    :param response: requests.Response 对象
    :param log: logging.Logger 对象
    """

    assert response.status_code == 200, f"请求失败，接口状态码：{response.status_code}"
    assert response.json().get('code') == 200, f"预期返回 系统内部状态码200，实际收到：{response.json().get('code')}"
