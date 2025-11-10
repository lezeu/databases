import time
import matplotlib.pyplot as plt
import numpy as np
from generate_data import generate_data
from get_top_5_sql import get_top_5_sql
from get_top_5_redis import get_top_5_redis
import io
import sys


def measure_performance(size, runs=5):
    """Measure average query time for both SQL and Redis."""
    print(f"\nTesting size {size}...")
    
    # Generate data
    generate_data(size)
    
    sql_times = []
    redis_times = []
    
    # Suppress output during timing
    for _ in range(runs):
        # Time SQL
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        start = time.time()
        get_top_5_sql()
        sql_time = time.time() - start
        sys.stdout = old_stdout
        sql_times.append(sql_time * 1000)  # Convert to ms
        
        # Time Redis
        sys.stdout = io.StringIO()
        start = time.time()
        get_top_5_redis()
        redis_time = time.time() - start
        sys.stdout = old_stdout
        redis_times.append(redis_time * 1000)  # Convert to ms
    
    return np.mean(sql_times), np.mean(redis_times)


def create_performance_plots():
    """Generate comparison plots between SQL and Redis."""
    
    # Test different data sizes
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    # sizes = [100, 500, 1000, 5000, 10000]
    sql_times = []
    redis_times = []
    
    print("Running performance tests...")
    print("This may take a few minutes...\n")
    
    for size in sizes:
        sql_avg, redis_avg = measure_performance(size, runs=3)
        sql_times.append(sql_avg)
        redis_times.append(redis_avg)
        print(f"Size {size}: SQL={sql_avg:.2f}ms, Redis={redis_avg:.2f}ms")
    
    # Create figure with 3 subplots (removed log scale)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Redis vs SQL Performance Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: Line chart - Query time vs Dataset size
    ax1 = axes[0]
    ax1.plot(sizes, sql_times, marker='o', linewidth=2, label='SQL', color='#3498db', markersize=8)
    ax1.plot(sizes, redis_times, marker='s', linewidth=2, label='Redis', color='#e74c3c', markersize=8)
    ax1.set_xlabel('Dataset Size (number of products)', fontsize=11)
    ax1.set_ylabel('Query Time (ms)', fontsize=11)
    ax1.set_title('Query Time vs Dataset Size', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Bar chart - Direct comparison
    ax2 = axes[1]
    x = np.arange(len(sizes))
    width = 0.35
    ax2.bar(x - width/2, sql_times, width, label='SQL', color='#3498db', alpha=0.8)
    ax2.bar(x + width/2, redis_times, width, label='Redis', color='#e74c3c', alpha=0.8)
    ax2.set_xlabel('Dataset Size', fontsize=11)
    ax2.set_ylabel('Query Time (ms)', fontsize=11)
    ax2.set_title('Side-by-Side Comparison', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(sizes)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Speedup factor
    ax3 = axes[2]
    speedup = [sql/redis for sql, redis in zip(sql_times, redis_times)]
    ax3.plot(sizes, speedup, marker='D', linewidth=2, color='#2ecc71', markersize=8)
    ax3.axhline(y=1, color='gray', linestyle='--', label='Equal performance')
    ax3.set_xlabel('Dataset Size', fontsize=11)
    ax3.set_ylabel('Speedup Factor (SQL time / Redis time)', fontsize=11)
    ax3.set_title('Redis Speedup Over SQL', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Add speedup values on points
    for i, (size, speed) in enumerate(zip(sizes, speedup)):
        ax3.annotate(f'{speed:.1f}x', (size, speed), 
                    textcoords="offset points", xytext=(0,10), 
                    ha='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    
    # Save the figure
    output_file = '../performance_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✅ Plot saved to: {output_file}")
    
    # Show statistics
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print(f"{'Size':<10} {'SQL (ms)':<12} {'Redis (ms)':<12} {'Speedup':<10}")
    print("-"*60)
    for size, sql_t, redis_t, speed in zip(sizes, sql_times, redis_times, speedup):
        print(f"{size:<10} {sql_t:<12.2f} {redis_t:<12.2f} {speed:<10.1f}x")
    print("="*60)
    
    # Show the plot
    plt.show()


if __name__ == "__main__":
    create_performance_plots()
