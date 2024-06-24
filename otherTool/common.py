import time
from functools import wraps

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
