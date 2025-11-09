from src.connection import r

def get_top_5_redis():
    top_products = list(r.zrevrange("top_products:rating", 0, 4, withscores=True))  # type: ignore
    print("Top 5 Products from Redis:")
    for rank, (product_id, score) in enumerate(top_products, 1):
        product_data = dict(r.hgetall(f"product:{product_id.decode()}"))  # type: ignore
        print(f"{rank}. Product {product_id.decode()}: {product_data[b'name'].decode()} - Rating: {float(score):.2f}")

if __name__ == "__main__":
    get_top_5_redis()
