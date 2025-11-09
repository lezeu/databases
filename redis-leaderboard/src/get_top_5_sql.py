from src.db_utils import connect_db

def get_top_5_sql():
    conn = connect_db("online_shopping")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.id, p.name, AVG(r.rating) as avg_rating
            FROM products p
            LEFT JOIN reviews r ON p.id = r.product_id
            GROUP BY p.id, p.name
            ORDER BY avg_rating DESC
            LIMIT 5
        """)
        top_products = cur.fetchall()
    conn.close()
    print("Top 5 Products from SQL:")
    for rank, (product_id, name, avg_rating) in enumerate(top_products, 1):
        print(f"{rank}. Product {product_id}: {name} - Rating: {avg_rating:.2f}" if avg_rating else f"{rank}. Product {product_id}: {name} - No ratings")

if __name__ == "__main__":
    get_top_5_sql()
