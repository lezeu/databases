import time
from generate_data import generate_data
from get_top_5_sql import get_top_5_sql
from get_top_5_redis import get_top_5_redis


def demo():
    sizes = [1000, 10000, 100000]  # Adjusted for feasibility
    results = {}

    for size in sizes:
        print(f"\n=== Demo for size {size} ===")

        # Generate data
        print("Generating data...")
        start_gen = time.time()
        generate_data(size)
        gen_time = time.time() - start_gen
        print(f"Data generation time: {gen_time:.2f}s")

        # Run queries 3 times
        print("Running queries...")
        redis_times = []
        sql_times = []

        # for _ in range(3):
        # Time SQL
        start_sql = time.time()
        get_top_5_sql()
        sql_times.append(time.time() - start_sql)

        # Time Redis
        start_redis = time.time()
        get_top_5_redis()
        redis_times.append(time.time() - start_redis)

        avg_sql = sum(sql_times) / len(sql_times)
        avg_redis = sum(redis_times) / len(redis_times)

        print(f"Average SQL time: {avg_sql:.4f}s")
        print(f"Average Redis time: {avg_redis:.4f}s")

        results[size] = {
            # "gen_time": gen_time,
            "avg_sql": avg_sql,
            "avg_redis": avg_redis
        }

    print("\n=== Summary ===")
    for size, data in results.items():
        # print(f"Size {size}: Gen {data['gen_time']:.2f}s, SQL {data['avg_sql']:.4f}s, Redis {data['avg_redis']:.4f}s")
        print(f"Size {size}: SQL {data['avg_sql']:.4f}s, Redis {data['avg_redis']:.4f}s")

if __name__ == "__main__":
    demo()
