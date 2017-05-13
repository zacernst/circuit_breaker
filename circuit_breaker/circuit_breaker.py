"""
A decorator for putting a timeout on a function. If the timeout
is exceeded, then a different function is called and its value
is returned.
"""

import time
import threading
import random


def circuit_breaker(timeout=None, timeout_function=None):
    """
    Decorator to enable a timeout on a function. If the decorated
    function does not complete in less than ``timeout`` seconds,
    then execute the function called ``timeout_function``, passing
    the original arguments to it.

    Args:
        timeout (float): Maximum number of seconds allowed for the
            function to execute.
        timeout_function (func): The function to be executed if the
            timeout is exceeded.
    """

    def decorator(func):
        
        def new_func(f, *args, **kwargs):
            """
            Threads cannot return any values. So we pass a mutable
            object (a list containing a ``None`` object) through
            the ``**kwargs`` and store the result of the function in
            there so that it can be retrieved outside the thread.
            But we do **not** want to pass a keyword argument to
            the function which the function isn't expecting. So we
            create a new reference to the mutable object
            (``_thread_result``), delete the corresponding key
            from the dictionary, and then re-insert it after the
            function has been called.
            """

            _thread_result = kwargs['_thread_result']
            del kwargs['_thread_result']
            result = f(*args, **kwargs)
            _thread_result[0] = result
            kwargs['_thread_result'] = _thread_result

        def wrapper(*args, **kwargs):
            thread_result = [None]
            kwargs['_thread_result'] = thread_result
            function_thread = threading.Thread(
                target=new_func,
                args=(func,) + args,
                kwargs=kwargs)
            function_thread.setDaemon(True)
            start_time = time.time()
            deadline = start_time + timeout
            function_thread.start()
            while function_thread.isAlive() and time.time() < deadline:
                pass
            deadline_exceeded = function_thread.isAlive()
            if deadline_exceeded:
                """
                The timeout has finished, but the thread is still alive,
                indicating that the function hasn't completed quickly
                enough. So call the backup.

                We don't use threads for this call, so we'll get rid of
                the ``_thread_result`` key in the ``**kwargs``.
                """
                del kwargs['_thread_result']
                return timeout_function(*args, **kwargs)
            return thread_result[0]
        return wrapper
    return decorator

if __name__ == '__main__':
    """
    Example. if ``foo`` isn't completed in under one second, then
    execute ``backup_function`` instead.
    """

    def backup_function(x):
        return 'I am in the backup function'


    @circuit_breaker(timeout=1, timeout_function=backup_function)
    def foo(x):
        time.sleep(2 * random.random())
        return 'the function finished in time: ' + str(x+1)


    print foo(1)
