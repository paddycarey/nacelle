# stdlib imports
import logging
import time


def retry_on_exception(exception_to_check, tries=4, delay=0.5, backoff=2):

    """
    Retry calling the decorated function using an exponential backoff.

    exception_to_check (Exception/tuple): the exception(s) to check
    tries (int): number of times to try before giving up
    delay (int/float): initial delay between retries in seconds
    backoff (int/float): backoff multiplier
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            try_one_last_time = True
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                    try_one_last_time = False
                    break
                except exception_to_check, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    logging.warning(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            if try_one_last_time:
                return f(*args, **kwargs)
            return
        return f_retry
    return deco_retry
