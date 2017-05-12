# Circuit breaker

Python decorator to implement timeout on functions. If the timeout is exceeded, a backup function is immediately executed and its value is returned.

## Installation

Just use pip:

```
pip install circuit_breaker
```

## Usage

If a service starts to have degraded performance and takes too long
to run, it could cause downstream services to slow down. Depending on
what services are affected, this may be unacceptable. For this reason,
it's useful to put a time limit on how long a function is permitted to
take. If the time limit is exceeded, a "backup" function could be
called instead, which would be more likely to execute quickly.

In engineering parlance, this is called a "circuit breaker" because it
prevents an overloaded system from causing other systems to fail. That's
what `circuit_breaker` does. Here's an example of how to use it:

```
import random
import sleep

from circuit_breaker import circuit_breaker

def bro(x, **kwargs):
    return 'bro'

@circuit_breaker(timeout=1, timeout_function=bro)  # pass function
def dude(x, **kwargs):
    time.sleep(random.random() * 2)
    return 'dude'
```

In the example, there is a function called `dude`, which will take
a random amount of time to run. If it takes more than one second, then
the `bro` function will be called. There are just two arguments
that have to be passed to the decorator: `timeout` which is an `int`
or a `float`, and `timeout_function`, which is a function.

There is one potential "gotcha" to be aware of. Because decorators are
applied by Python at compile time, the `timeout_function` has to be
defined *before* the decorator. In other words, if we moved the
definition of the `bro` function to the end of the script, it would fail
miserably and you'd be sad.
