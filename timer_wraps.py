import functools
from functools import wraps

print_flush = functools.partial(print, flush=True)
import time

def measure_time(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):

        start_time = time.perf_counter()

        try:
            result = f(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            print_flush('Function "{}": {}s'.format(f.__name__, elapsed))
        return elapsed
    return _wrapper
