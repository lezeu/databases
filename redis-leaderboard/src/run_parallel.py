import time

import matplotlib.pyplot as plt
from get_top_5_redis import get_top_5_redis
from get_top_5_sql import get_top_5_sql


def run_queries(num_runs=5, save_plot=False):
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
    
    # Generate plot if requested
    if save_plot:
        create_comparison_plot(sql_times, redis_times)
    
    return sql_times, redis_times


def create_comparison_plot(sql_times, redis_times):
    """Create a simple comparison plot of the runs."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Query Performance Comparison', fontsize=14, fontweight='bold')
    
    runs = list(range(1, len(sql_times) + 1))
    
    # Plot 1: Line chart of each run
    ax1.plot(runs, [t*1000 for t in sql_times], marker='o', label='SQL', 
             color='#3498db', linewidth=2)
    ax1.plot(runs, [t*1000 for t in redis_times], marker='s', label='Redis', 
             color='#e74c3c', linewidth=2)
    ax1.set_xlabel('Run Number', fontsize=11)
    ax1.set_ylabel('Query Time (ms)', fontsize=11)
    ax1.set_title('Individual Run Times', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Bar chart of averages
    avg_sql = sum(sql_times) / len(sql_times) * 1000
    avg_redis = sum(redis_times) / len(redis_times) * 1000
    
    databases = ['SQL', 'Redis']
    averages = [avg_sql, avg_redis]
    colors = ['#3498db', '#e74c3c']
    
    bars = ax2.bar(databases, averages, color=colors, alpha=0.8, width=0.6)
    ax2.set_ylabel('Average Query Time (ms)', fontsize=11)
    ax2.set_title('Average Performance', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, avg in zip(bars, averages):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{avg:.2f}ms',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Add speedup text
    speedup = avg_sql / avg_redis
    ax2.text(0.5, max(averages) * 0.9, f'Speedup: {speedup:.1f}x', 
             ha='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#2ecc71', alpha=0.7))
    
    plt.tight_layout()
    
    # Save the plot
    output_file = '../query_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n📊 Plot saved to: {output_file}")


if __name__ == "__main__":
    import sys
    num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    save_plot = '--plot' in sys.argv or '-p' in sys.argv
    run_queries(num_runs, save_plot)


