from src.connection import r
import time
import random
from src.db_utils import connect_db

def insert_reviews_sql(product_id, num_reviews, rating=5):
    conn = connect_db("online_shopping")
    with conn.cursor() as cur:
        for i in range(num_reviews):
            user_id = random.randint(1, 10)  # Use existing users
            # Insert review
            cur.execute("INSERT INTO reviews (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)", (user_id, product_id, rating, f"Great product {i}!"))
    conn.commit()
    conn.close()
    print(f"Inserted {num_reviews} reviews to product {product_id} in SQL")

def insert_reviews_redis(product_id, num_reviews, rating=5.0):
    review_id = int(r.incr("review_id_counter"))  # type: ignore
    for i in range(num_reviews):
        user_id = random.randint(1, 10)  # Use existing users
        # Add review
        r.hset(f"review:{review_id}", mapping={
            "user_id": str(user_id),
            "product_id": str(product_id),
            "rating": str(rating),
            "comment": f"Great product {i}!",
            "created_at": str(time.time())
        })
        r.sadd(f"reviews:{product_id}", review_id)
        r.sadd(f"reviews:{user_id}", review_id)
        review_id += 1
    # Update top_products:rating
    reviews = list(r.smembers(f"reviews:{product_id}"))  # type: ignore
    if reviews:
        ratings = [float(r.hget(f"review:{rid.decode()}", "rating")) for rid in reviews]  # type: ignore
        avg_rating = sum(ratings) / len(ratings)
        r.zadd("top_products:rating", {str(product_id): avg_rating})
    print(f"Inserted {num_reviews} reviews to product {product_id} in Redis")

def insert_reviews(product_id, num_reviews, rating=5):
    insert_reviews_sql(product_id, num_reviews, rating)
    insert_reviews_redis(product_id, num_reviews, rating)

if __name__ == "__main__":
    # Change top by adding reviews to product 10
    insert_reviews(10, 100, 5)
