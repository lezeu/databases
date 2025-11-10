"""
Performance comparison script (refactored).
Follows KISS principle - simple and clear.
"""
from performance_utils import timer
from get_top_5_redis import get_top_5_redis
from get_top_5_sql import get_top_5_sql


def run_queries(num_runs=5):
    """
    Run performance comparison between SQL and Redis.
    
    Args:
        num_runs: Number of times to run each query
    """
    redis_times = []
    sql_times = []

    for i in range(num_runs):
        print(f"\nRun {i+1}:")

        # Time SQL
        with timer() as t:
            get_top_5_sql()
        sql_times.append(t.elapsed)

        # Time Redis  
        with timer() as t:
            get_top_5_redis()
        redis_times.append(t.elapsed)

    # Calculate averages
    avg_sql = sum(sql_times) / len(sql_times)
    avg_redis = sum(redis_times) / len(redis_times)

    # Display results
    print(f"\n{'='*60}")
    print(f"PERFORMANCE COMPARISON ({num_runs} runs)")
    print(f"{'='*60}")
    print(f"Average SQL query time:   {avg_sql:.2f}ms")
    print(f"Average Redis query time: {avg_redis:.2f}ms")
    print(f"{'='*60}")
    
    if avg_sql > avg_redis:
        speedup = avg_sql / avg_redis
        print(f"🚀 Redis is {speedup:.1f}x FASTER than SQL!")
    
    print(f"{'='*60}")
    
    return sql_times, redis_times


if __name__ == "__main__":
    import sys
    num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_queries(num_runs)
