.. Circuit Breaker documentation master file, created by
   sphinx-quickstart on Sat May 13 09:01:30 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Circuit Breaker
==========================

The circuit breaker package contains a decorator that you can apply to
your Python function, which will prevent it from running longer than
a specified timeout. If the timeout is reached, a "backup function" is
run immediately and its value is returned.

I wrote this decorator in order to guarantee that a microservice never
takes too long to return a result, avoiding degradation of downstream
services.

To install it, just use ``pip``:

::

    pip install circuit_breaker

To use it, decorate your function in the normal way, providing two
keyword arguments: ``timeout`` and ``timeout_function``. Here is an
example of a function that takes longer than one second to run half
of the times it's called. When one second has elapsed, a backup function
is called immediately.

::

    def backup_function(x):
        return 'I am in the backup function'


    @circuit_breaker(timeout=1, timeout_function=backup_function)
    def slow_function(x):
        time.sleep(2 * random.random())
        return 'the function finished in time: ' + str(x)
                                    
A potential "gotcha" when using this decorator is that because
decorators are always applied at compile time, the function
you use as your ``backup_function`` must be defined **before**
the decorated function. In other words, if we were to move
the ``backup_function`` in the example to a position after
``slow_function``, we'd get a compile-time error, which would
make us sad.

Contact zac.ernst@gmail.com with questions/comments/concerns/threats.

http://github.com/zacernst/circuit_breaker
