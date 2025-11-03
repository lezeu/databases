import psycopg2

def connect_db(db_name):
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database=db_name,
        user="postgres",
        password="password"
    )