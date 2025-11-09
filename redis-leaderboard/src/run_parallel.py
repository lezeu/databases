import time
from get_top_5_redis import get_top_5_redis
from get_top_5_sql import get_top_5_sql


def run_queries(num_runs=5):
    redis_times = []
    sql_times = []

    for i in range(num_runs):
        print(f"\nRun {i+1}:")

        # Time SQL first
        start_sql = time.time()
        get_top_5_sql()
        sql_times.append(time.time() - start_sql)

        # Time Redis
        start_redis = time.time()
        get_top_5_redis()
        redis_times.append(time.time() - start_redis)

    avg_redis = sum(redis_times) / len(redis_times)
    avg_sql = sum(sql_times) / len(sql_times)

    print(f"\n{'='*60}")
    print(f"PERFORMANCE COMPARISON ({num_runs} runs)")
    print(f"{'='*60}")
    print(f"Average SQL query time:   {avg_sql:.4f}s ({avg_sql*1000:.1f}ms)")
    print(f"Average Redis query time: {avg_redis:.4f}s ({avg_redis*1000:.1f}ms)")
    print(f"{'='*60}")
    if avg_sql > avg_redis:
        speedup = avg_sql / avg_redis
        print(f"🚀 Redis is {speedup:.1f}x FASTER than SQL!")
    print(f"{'='*60}")


if __name__ == "__main__":
    import sys
    num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_queries(num_runs)

