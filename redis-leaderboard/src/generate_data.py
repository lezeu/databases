from connection import r
import random
import time
from db_utils import connect_db
import psycopg2

def create_database_if_not_exists():
    """Create the online_shopping database if it doesn't exist"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="password"
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            # Check if database exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname='online_shopping'")
            exists = cur.fetchone()
            if not exists:
                cur.execute("CREATE DATABASE online_shopping")
                print("Database 'online_shopping' created")
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def create_schema():
    """Create tables in the database"""
    conn = connect_db("online_shopping")
    with conn.cursor() as cur:
        # Create tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                total DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()
    print("Schema created successfully")

def generate_sql_data(size=10):
    create_database_if_not_exists()
    create_schema()
    conn = connect_db("online_shopping")
    with conn.cursor() as cur:
        # Clear existing data
        cur.execute("TRUNCATE TABLE reviews, orders, products, users RESTART IDENTITY CASCADE")
        # Users
        for i in range(1, size + 1):
            cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (f"user{i}", f"user{i}@example.com"))
        # Products
        for i in range(1, size + 1):
            cur.execute("INSERT INTO products (name, price, description) VALUES (%s, %s, %s)", (f"Product {i}", random.uniform(10, 100), f"Description {i}"))
        # Orders
        for i in range(1, size * 2):
            user_id = random.randint(1, size)
            cur.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s)", (user_id, random.uniform(20, 200)))
        # Reviews
        for i in range(1, size * 5):
            user_id = random.randint(1, size)
            product_id = random.randint(1, size)
            rating = random.randint(1, 5)
            cur.execute("INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)", (user_id, product_id, rating, f"Review {i}"))
    conn.commit()
    conn.close()
    print(f"SQL data generated for size {size}")

def generate_redis_data(size=10):
    r.flushdb()
    # Users
    for i in range(1, size + 1):
        r.hset(f"user:{i}", mapping={"username": f"user{i}", "email": f"user{i}@example.com", "created_at": str(time.time())})
    # Products
    for i in range(1, size + 1):
        r.hset(f"product:{i}", mapping={"name": f"Product {i}", "price": str(random.uniform(10, 100)), "description": f"Description {i}", "created_at": str(time.time())})
    # Orders
    order_id = 1
    for i in range(1, size * 2):
        user_id = random.randint(1, size)
        total = random.uniform(20, 200)
        r.hset(f"order:{order_id}", mapping={"user_id": str(user_id), "total": str(total), "created_at": str(time.time())})
        r.sadd(f"orders:{user_id}", order_id)
        order_id += 1
    # Reviews
    review_id = 1
    for i in range(1, size * 5):
        user_id = random.randint(1, size)
        product_id = random.randint(1, size)
        rating = random.randint(1, 5)
        r.hset(f"review:{review_id}", mapping={
            "user_id": str(user_id),
            "product_id": str(product_id),
            "rating": str(rating),
            "comment": f"Review {i}",
            "created_at": str(time.time())
        })
        r.sadd(f"reviews:{product_id}", review_id)
        r.sadd(f"reviews:{user_id}", review_id)
        review_id += 1
    # Update top_products:rating
    for pid in range(1, size + 1):
        reviews = list(r.smembers(f"reviews:{pid}"))  # type: ignore
        if reviews:
            ratings = [float(r.hget(f"review:{rid.decode()}", "rating")) for rid in reviews]  # type: ignore
            avg_rating = sum(ratings) / len(ratings)
            r.zadd("top_products:rating", {str(pid): avg_rating})
    print(f"Redis data generated for size {size}")

def generate_data(size=10):
    # Set random seed for reproducibility
    random.seed(42)
    generate_sql_data(size)
    random.seed(42)  # Reset seed for Redis to match SQL
    generate_redis_data(size)

if __name__ == "__main__":
    import sys
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    generate_data(size)
