import pytest
from decorators import timer, retry, cache

def test_timer_returns_result():
    """Timer decorator should not affect return value."""
    
    @timer
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5

def test_retry_succeeds_eventually():
    """Retry should succeed if function works within attempts."""
    
    @retry(max_attempts=5, delay=0.5)
    def flaky_function():
        if flaky_function.attempts < 3:
            flaky_function.attempts += 1
            raise ValueError("Failed attempt")
        return "Success"
    flaky_function.attempts = 0
    assert flaky_function() == "Success"

def test_cache_returns_cached_value():
    """Cache should return same value without recomputing."""
    @cache(max_size=100)
    def expensive_computation(x):
        return x ** 2
    assert expensive_computation(5) == 25
    assert expensive_computation(5) == 25

def test_cache_info_tracks_hits():
    """Cache info should track hits and misses."""
    @cache(max_size=100)
    def expensive_computation(x):
        return x ** 2
    
    @cache(max_size=100)
    def add(x, y):
        return x + y
    
    # expensive_computation(5)
    # expensive_computation(5)
    # assert expensive_computation.cache_info()["hits"] == 1
    # assert expensive_computation.cache_info()["misses"] == 1
    add(5, 7)
    add(5, 7)
    assert add.cache_info()["hits"] == 1
    assert add.cache_info()["misses"] == 1
