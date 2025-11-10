"""
Performance measurement utilities (DRY principle).
Centralized timing logic to avoid code duplication.
"""
import time
from contextlib import contextmanager


@contextmanager
def timer():
    """
    Context manager for timing code execution.
    
    Usage:
        with timer() as t:
            # code to time
            pass
        print(f"Took {t.elapsed}ms")
    """
    class TimerResult:
        def __init__(self):
            self.start = time.time()
            self.elapsed = 0
        
        def stop(self):
            self.elapsed = (time.time() - self.start) * 1000  # Convert to ms
    
    result = TimerResult()
    try:
        yield result
    finally:
        result.stop()


def measure_query_time(query_func, runs=1):
    """
    Measure average query execution time.
    
    Args:
        query_func: Function to execute
        runs: Number of times to run
    
    Returns:
        Average time in milliseconds
    """
    times = []
    for _ in range(runs):
        with timer() as t:
            query_func()
        times.append(t.elapsed)
    
    return sum(times) / len(times) if times else 0


def format_time(milliseconds):
    """Format time in human-readable way."""
    if milliseconds < 1:
        return f"{milliseconds * 1000:.2f}μs"
    elif milliseconds < 1000:
        return f"{milliseconds:.2f}ms"
    else:
        return f"{milliseconds / 1000:.2f}s"
