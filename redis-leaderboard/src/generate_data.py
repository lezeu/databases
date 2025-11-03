from .connection import r
import random
import time
from .db_utils import connect_db

def generate_sql_data():
    conn = connect_db("online_shopping")
    with conn.cursor() as cur:
        # Users
        for i in range(1, 11):
            cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (f"user{i}", f"user{i}@example.com"))
        # Products
        for i in range(1, 11):
            cur.execute("INSERT INTO products (name, price, description) VALUES (%s, %s, %s)", (f"Product {i}", random.uniform(10, 100), f"Description {i}"))
        # Orders
        for i in range(1, 21):
            user_id = random.randint(1, 10)
            cur.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s)", (user_id, random.uniform(20, 200)))
        # Reviews
        for i in range(1, 51):
            user_id = random.randint(1, 10)
            product_id = random.randint(1, 10)
            rating = random.randint(1, 5)
            cur.execute("INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)", (user_id, product_id, rating, f"Review {i}"))
    conn.commit()
    conn.close()
    print("SQL data generated")

def generate_redis_data():
    r.flushdb()
    # Users
    for i in range(1, 11):
        r.hset(f"user:{i}", mapping={"username": f"user{i}", "email": f"user{i}@example.com", "created_at": str(time.time())})
    # Products
    for i in range(1, 11):
        r.hset(f"product:{i}", mapping={"name": f"Product {i}", "price": str(random.uniform(10, 100)), "description": f"Description {i}", "created_at": str(time.time())})
    # Orders
    order_id = 1
    for i in range(1, 21):
        user_id = random.randint(1, 10)
        total = random.uniform(20, 200)
        r.hset(f"order:{order_id}", mapping={"user_id": str(user_id), "total": str(total), "created_at": str(time.time())})
        r.sadd(f"orders:{user_id}", order_id)
        order_id += 1
    # Reviews
    review_id = 1
    for i in range(1, 51):
        user_id = random.randint(1, 10)
        product_id = random.randint(1, 10)
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
    for pid in range(1, 11):
        reviews = list(r.smembers(f"reviews:{pid}"))  # type: ignore
        if reviews:
            ratings = [float(r.hget(f"review:{rid.decode()}", "rating")) for rid in reviews]  # type: ignore
            avg_rating = sum(ratings) / len(ratings)
            r.zadd("top_products:rating", {str(pid): avg_rating})
    print("Redis data generated")

def generate_data():
    generate_sql_data()
    generate_redis_data()

if __name__ == "__main__":
    generate_data()
