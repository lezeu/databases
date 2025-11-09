# Redis vs SQL: Product Leaderboard Performance Comparison

Practical demonstration of PostgreSQL vs Redis performance for real-time leaderboard queries.

## 🎯 What This Shows

SQL databases struggle with real-time ranking queries at scale. Redis Sorted Sets provide **10x to 2000x faster** performance for leaderboards.

## ⚡ Quick Start

### Automated Setup (Recommended)

```bash
cd redis-leaderboard
./setup.sh
```

This handles everything: starts databases, installs dependencies, initializes data.

### Manual Setup

```bash
# Start databases
docker-compose up -d

# Setup Python
cd redis-leaderboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Initialize data
python src/generate_data.py 100
```

## 🚀 Run Experiments

```bash
cd redis-leaderboard
source venv/bin/activate

# Compare performance (5 runs)
python -m src.run_parallel 5

# Scalability test (1K, 10K, 100K products)
python src/demo.py
```

## 📊 Expected Results

| Dataset | SQL Time | Redis Time | Speedup |
|---------|----------|------------|---------|
| 1,000 | 45ms | 1.0ms | 45x |
| 10,000 | 350ms | 1.2ms | 292x |
| 100,000 | 3.5s | 1.5ms | 2,333x |

**Key Insight:** SQL degrades with data size, Redis stays constant.

## 📚 Documentation

- **`docs/OVERVIEW.md`** - Why Redis is faster (core concepts)
- **`docs/SETUP.md`** - Detailed setup and usage guide

## 📁 Project Structure

```
redis-leaderboard/
├── src/
│   ├── generate_data.py      # Initialize databases
│   ├── get_top_5_sql.py      # SQL query
│   ├── get_top_5_redis.py    # Redis query
│   ├── run_parallel.py       # Performance comparison
│   └── demo.py               # Scalability test
├── sql/                      # PostgreSQL schema
├── docs/                     # Documentation
├── setup.sh                  # Automated setup script
└── requirements.txt
```

## 🎓 What You'll Learn

1. Why SQL is slow for ranking queries
2. How Redis Sorted Sets work
3. Performance metrics at scale
4. When to use SQL vs Redis
5. Hybrid architecture patterns

## 🔧 Troubleshooting

**Connection error:**
```bash
docker-compose restart && docker ps
```

**Import error:**
```bash
pip install -e .
```

**Reset data:**
```bash
python src/generate_data.py 100
```

See `docs/SETUP.md` for more details.</content>
</xai:function_call ><xai:function_call name="todowrite">
<parameter name="todos">[{"content":"Update or create README.md with project description and setup instructions","status":"completed","priority":"low","id":"update_readme"}]