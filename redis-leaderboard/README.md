# Online Shopping Database Comparison: SQL vs Redis

This project demonstrates a comparison between PostgreSQL (SQL) and Redis (NoSQL) for an Online Shopping application, focusing on querying top products by rating and performance evaluation.

## Setup

1. Ensure Docker is installed and running.
2. Pull and run PostgreSQL and Redis:
   ```bash
   docker run -d --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
   docker run -d --name redis -p 6379:6379 redis
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Schemas

- **SQL (PostgreSQL)**: Tables for users, products, orders, reviews.
- **Redis**: Hashes for entities, sets for relationships, sorted sets for rankings.

## Scripts

- `src/generate_data.py`: Generates sample data (10 users, 10 products, orders, reviews).
- `src/get_top_5_sql.py`: Queries top 5 products by rating from SQL.
- `src/get_top_5_redis.py`: Queries top 5 products by rating from Redis.
- `src/run_parallel.py`: Runs both queries sequentially and measures times.
- `src/insert_reviews.py`: Inserts reviews to a product to change rankings.

## Usage

1. Generate data:
   ```bash
   python src/generate_data.py
   ```

2. Run top 5 queries:
   ```bash
   python -m src.run_parallel  # 5 runs by default
   python -m src.run_parallel 10  # Specify number of runs
   ```

3. Run scalability demo:
   ```bash
   python -m src.demo  # Tests sizes 100, 1000, 10000
   ```

3. Insert reviews to change top (e.g., boost product 10):
   ```bash
   python src/insert_reviews.py
   ```

4. Run queries again to see updated rankings.

## Results

- Redis typically faster for reads due to in-memory storage.
- SQL provides ACID compliance and complex queries.
- Parallel execution shows real-time performance differences.

## Improvements

- Add larger datasets for scalability testing.
- Implement error handling and logging.
- Add visualizations for performance metrics.
- Use async Redis for concurrent operations.</content>
</xai:function_call ><xai:function_call name="todowrite">
<parameter name="todos">[{"content":"Update or create README.md with project description and setup instructions","status":"completed","priority":"low","id":"update_readme"}]