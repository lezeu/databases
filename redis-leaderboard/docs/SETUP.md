# Setup and Usage Guide

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.8+

## 🚀 Automated Setup (Recommended)

```bash
cd redis-leaderboard
./setup.sh
```

This automatically:
1. Starts PostgreSQL & Redis containers
2. Creates Python virtual environment  
3. Installs all dependencies
4. Initializes databases
5. Generates 100 sample products

**Done!** Skip to [Running Experiments](#running-experiments)

## 🔧 Manual Setup

### Step 1: Start Databases

```bash
docker-compose up -d  # From project root
docker ps  # Verify containers running
```

### Step 2: Python Environment

```bash
cd redis-leaderboard
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Step 3: Initialize Data

```bash
cd src
python generate_data.py 100
```

## 🔬 Running Experiments

### Basic Performance Comparison

```bash
source venv/bin/activate  # If not already activated
cd src
python run_parallel.py 5
```

**With Visualization:**
```bash
python run_parallel.py 5 --plot
```
This generates a `query_comparison.png` plot showing the performance differences.

**Output:**
```
Average SQL query time: 0.0096s
Average Redis query time: 0.0028s
Redis is 3.4x faster!

📊 Plot saved to: ../query_comparison.png
```

### Scalability Test

Tests performance at 1K, 10K, and 100K products:

```bash
cd src
python demo.py
```

Shows how SQL degrades while Redis stays constant.

### Comprehensive Performance Visualization

Generate detailed performance comparison plots across multiple dataset sizes:

```bash
cd src
python visualize_performance.py
```

This will:
- Test performance at 100, 500, 1K, 5K, and 10K products
- Generate 3 comprehensive plots showing:
  - Query time vs dataset size
  - Side-by-side comparison
  - Speedup factor over dataset size
- Save results to `performance_comparison.png`

**Note:** This takes 5-10 minutes as it generates multiple datasets.

### Individual Queries

```bash
cd src
python get_top_5_sql.py    # Query SQL only
python get_top_5_redis.py  # Query Redis only
```

### Simulate Real-time Updates

Add 100 five-star reviews to boost a product:

```bash
cd src
python insert_reviews.py
python run_parallel.py 1  # See updated rankings
```

## 📊 Understanding Results

```
Size 1000: SQL 45ms, Redis 1.0ms     (45x faster)
Size 10000: SQL 350ms, Redis 1.2ms   (292x faster)
Size 100000: SQL 3.5s, Redis 1.5ms   (2,333x faster)
```

**Key Insight:** SQL performance degrades with data size, Redis stays constant.

## 🧪 Advanced Usage

### Custom Dataset Sizes

```bash
cd src
python generate_data.py 5000   # 5K products
python generate_data.py 10000  # 10K products
```

**Note:** 100K products takes ~30-60 seconds to generate.

### Statistical Analysis

```bash
cd src
python run_parallel.py 100  # 100 runs for statistics
```

### Monitor Databases

**PostgreSQL:**
```bash
docker exec -it postgres psql -U postgres -d online_shopping

SELECT COUNT(*) FROM reviews;
SELECT pg_size_pretty(pg_total_relation_size('reviews'));
\q
```

**Redis:**
```bash
docker exec -it redis redis-cli

KEYS *
ZCARD top_products:rating
ZREVRANGE top_products:rating 0 4 WITHSCORES
exit
```

## 🔧 Troubleshooting

### Database Connection Error

```bash
docker-compose restart
docker ps  # Verify running
```

### Import/Module Errors

Make sure you're in the `src/` directory when running scripts:
```bash
cd redis-leaderboard/src
python run_parallel.py 5
```

### Data Inconsistency

```bash
cd src
python generate_data.py 100  # Regenerate data
```

### Redis Connection Test

```bash
docker exec redis redis-cli ping  # Should return PONG
```

## 🧹 Cleanup

**Stop (keep data):**
```bash
docker-compose down
```

**Stop and delete data:**
```bash
docker-compose down -v
```

**Clean Python cache:**
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
```

## 💡 Tips

- Use `docker stats` to monitor resource usage
- Check Redis memory: `docker exec redis redis-cli INFO memory`
- For large datasets, increase Docker memory allocation
- Run scripts from the `src/` directory for proper imports
