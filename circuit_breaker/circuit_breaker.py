"""
A decorator for putting a timeout on a function. If the timeout
is exceeded, then a different function is called and its value
is returned.
"""

from functools import wraps
import time
import threading
import random


def circuit_breaker(timeout=None, timeout_function=None):
    """
    Decorator to enable a timeout on a function. If the decorated
    functiond does not complete in less than ``timeout`` seconds,
    then execute the function called ``timeout_function``, passing
    the original arguments to it.

    Args:
        timeout (float): Maximum number of seconds allowed for the
            function to execute.
        timeout_function (func): The function to be executed if the
            timeout is exceeded.
    """

    def decorator(func):
        
        def new_func(*args, **kwargs):
            result = func(*args, **kwargs)
            kwargs['_thread_result'][0] = result

        def wrapper(*args, **kwargs):
            thread_result = [None]
            kwargs['_thread_result'] = thread_result
            function_thread = threading.Thread(
                target=new_func,
                args=args,
                kwargs=kwargs)
            function_thread.setDaemon(True)
            start_time = time.time()
            deadline = start_time + timeout
            function_thread.start()
            while function_thread.isAlive() and time.time() < deadline:
                pass
            deadline_exceeded = function_thread.isAlive()
            if deadline_exceeded:
                return timeout_function(*args, **kwargs)
            return thread_result[0]
        return wrapper
    return decorator

if __name__ == '__main__':
    """
    Example. if ``foo`` isn't completed in under one second, then
    execute ``backup_function`` instead.
    """

    def backup_function(x, **kwargs):
        return 'I am in the backup function'


    @circuit_breaker(timeout=1, timeout_function=backup_function)
    def foo(x, **kwargs):
        time.sleep(2 * random.random())
        return 'the function finished in time: ' + str(x+1)


    print foo(1)
