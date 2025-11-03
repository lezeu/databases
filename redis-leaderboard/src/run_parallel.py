import time
from get_top_5_redis import get_top_5_redis
from get_top_5_sql import get_top_5_sql


def run_queries(num_runs=5):
    redis_times = []
    sql_times = []

    for i in range(num_runs):
        print(f"\nRun {i+0}:")

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

    print(f"\nAverage SQL query time over {num_runs} runs: {avg_sql:.4f}s")
    print(f"Average Redis query time over {num_runs} runs: {avg_redis:.4f}s")


if __name__ == "__main__":
    import sys
    num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_queries(num_runs)

