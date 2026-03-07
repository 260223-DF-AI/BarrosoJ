from functools import wraps
from typing import Callable
import time
import logging

logging.basicConfig(level=logging.INFO)

def timer(func):
    """
    Measure and print function execution time.
    
    Usage:
        @timer
        def slow_function():
            time.sleep(1)
    
    Output: "slow_function took 1.0023 seconds"
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def logger(func):
    """
    Log function calls with arguments and return value.
    
    Usage:
        @logger
        def add(a, b):
            return a + b
        
        add(2, 3)
    
    Output:
        "Calling add(2, 3)"
        "add returned 5"
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result

    return wrapper


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Retry a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Seconds to wait between retries
        exceptions: Tuple of exceptions to catch
    
    Usage:
        @retry(max_attempts=3, delay=0.5)
        def flaky_api_call():
            # might fail sometimes
            pass
    """
    
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    # failed attempt, log and wait `delay` seconds
                    logging.warning(f"Attempt {i+1} failed with error: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


def cache(max_size=128):
    """
    Cache function results.
    Similar to lru_cache but with visible cache inspection.
    
    Usage:
        @cache(max_size=100)
        def expensive_computation(x):
            return x ** 2
        
        expensive_computation(5)  # Computes
        expensive_computation(5)  # Returns cached
        
        # Inspect cache
        expensive_computation.cache_info()
        expensive_computation.cache_clear()
    """
    cache: dict = {}
    cache_info = {
        "max_size": max_size,
        "curr_size": len(cache),
        "hits": 0,
        "misses": 0,
    }
    
    def decorator(func):
        func.cache_info = lambda : cache_info
        func.cache_clear = lambda : cache.clear()
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (args, tuple(sorted(kwargs.items())))
            if cache_key in cache:
                cache_info["hits"] += 1
                # put back into dict so that it is most recent in ordering
                cached_val = cache.pop(cache_key)
                cache[cache_key] = cached_val
                return cache[cache_key]
            # func call not already cached, call it
            else:
                cache_info["misses"] += 1
                result = func(*args, **kwargs)
                if len(cache) != max_size:
                    cache[cache_key] = result
                else:
                    val_to_delete = next(iter(cache)) # find least recent entry to remove
                    del cache[val_to_delete]
                    cache[cache_key] = result
            cache[cache_key] = result
            return result
        
        return wrapper
    return decorator

    


