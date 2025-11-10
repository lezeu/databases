"""
Data generation module following SOLID principles.
Single Responsibility: Each class handles one type of database.
"""
import random
import time
from config import get_postgres_connection, get_redis_connection, DatabaseConfig


class PostgreSQLDataGenerator:
    """Handles PostgreSQL data generation (Single Responsibility)."""
    
    def __init__(self):
        self.db_name = DatabaseConfig.PG_DATABASE
    
    def create_database(self):
        """Create database if it doesn't exist."""
        try:
            conn = get_postgres_connection("postgres")
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'")
                if not cur.fetchone():
                    cur.execute(f"CREATE DATABASE {self.db_name}")
                    print(f"Database '{self.db_name}' created")
            conn.close()
        except Exception as e:
            print(f"Error creating database: {e}")
    
    def create_schema(self):
        """Create tables."""
        conn = get_postgres_connection(self.db_name)
        
        schema_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                total DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
        conn.close()
        print("Schema created successfully")
    
    def clear_data(self):
        """Clear existing data."""
        conn = get_postgres_connection(self.db_name)
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE reviews, orders, products, users RESTART IDENTITY CASCADE")
        conn.commit()
        conn.close()
    
    def generate_data(self, size=10):
        """Generate test data."""
        conn = get_postgres_connection(self.db_name)
        
        with conn.cursor() as cur:
            # Insert users
            for i in range(1, size + 1):
                cur.execute(
                    "INSERT INTO users (username, email) VALUES (%s, %s)",
                    (f"user{i}", f"user{i}@example.com")
                )
            
            # Insert products
            for i in range(1, size + 1):
                cur.execute(
                    "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)",
                    (f"Product {i}", random.uniform(10, 100), f"Description {i}")
                )
            
            # Insert orders
            for _ in range(size * 2):
                user_id = random.randint(1, size)
                cur.execute(
                    "INSERT INTO orders (user_id, total) VALUES (%s, %s)",
                    (user_id, random.uniform(20, 200))
                )
            
            # Insert reviews
            for _ in range(size * 5):
                user_id = random.randint(1, size)
                product_id = random.randint(1, size)
                rating = random.randint(1, 5)
                cur.execute(
                    "INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)",
                    (user_id, product_id, rating, "Review comment")
                )
        
        conn.commit()
        conn.close()
        print(f"SQL data generated for size {size}")


class RedisDataGenerator:
    """Handles Redis data generation (Single Responsibility)."""
    
    def __init__(self):
        self.redis = get_redis_connection()
    
    def clear_data(self):
        """Clear all Redis data."""
        self.redis.flushdb()
    
    def generate_data(self, size=10):
        """Generate test data in Redis."""
        # Insert users
        for i in range(1, size + 1):
            self.redis.hset(
                f"user:{i}",
                mapping={
                    "username": f"user{i}",
                    "email": f"user{i}@example.com",
                    "created_at": str(time.time())
                }
            )
        
        # Insert products
        for i in range(1, size + 1):
            self.redis.hset(
                f"product:{i}",
                mapping={
                    "name": f"Product {i}",
                    "price": str(random.uniform(10, 100)),
                    "description": f"Description {i}",
                    "created_at": str(time.time())
                }
            )
        
        # Insert orders
        order_id = 1
        for _ in range(size * 2):
            user_id = random.randint(1, size)
            self.redis.hset(
                f"order:{order_id}",
                mapping={
                    "user_id": str(user_id),
                    "total": str(random.uniform(20, 200)),
                    "created_at": str(time.time())
                }
            )
            self.redis.sadd(f"orders:{user_id}", order_id)
            order_id += 1
        
        # Insert reviews and build leaderboard
        review_id = 1
        for _ in range(size * 5):
            user_id = random.randint(1, size)
            product_id = random.randint(1, size)
            rating = random.randint(1, 5)
            
            self.redis.hset(
                f"review:{review_id}",
                mapping={
                    "user_id": str(user_id),
                    "product_id": str(product_id),
                    "rating": str(rating),
                    "comment": "Review comment",
                    "created_at": str(time.time())
                }
            )
            self.redis.sadd(f"reviews:{product_id}", review_id)
            self.redis.sadd(f"reviews:{user_id}", review_id)
            review_id += 1
        
        # Calculate and store average ratings
        for pid in range(1, size + 1):
            reviews = list(self.redis.smembers(f"reviews:{pid}"))
            if reviews:
                ratings = [
                    float(self.redis.hget(f"review:{rid.decode()}", "rating"))
                    for rid in reviews
                ]
                avg_rating = sum(ratings) / len(ratings)
                self.redis.zadd("top_products:rating", {str(pid): avg_rating})
        
        print(f"Redis data generated for size {size}")


def generate_data(size=10):
    """
    Generate data for both databases.
    Uses the same random seed for reproducibility.
    """
    random.seed(42)
    
    # PostgreSQL
    pg_gen = PostgreSQLDataGenerator()
    pg_gen.create_database()
    pg_gen.create_schema()
    pg_gen.clear_data()
    pg_gen.generate_data(size)
    
    # Redis (reset seed for same randomness)
    random.seed(42)
    redis_gen = RedisDataGenerator()
    redis_gen.clear_data()
    redis_gen.generate_data(size)


if __name__ == "__main__":
    import sys
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    generate_data(size)
