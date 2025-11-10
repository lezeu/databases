"""PostgreSQL connection utilities."""
from config import get_postgres_connection


def connect_db(db_name):
    """Get PostgreSQL connection (legacy wrapper)."""
    return get_postgres_connection(db_name)
