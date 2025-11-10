"""
Configuration module for database connections.
Centralizes all database configuration to follow DRY principle.
"""
import redis
import psycopg2


class DatabaseConfig:
    """Database configuration (Single Responsibility Principle)."""
    
    # PostgreSQL settings
    PG_HOST = "localhost"
    PG_PORT = 5432
    PG_USER = "postgres"
    PG_PASSWORD = "password"
    PG_DATABASE = "online_shopping"
    
    # Redis settings
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0


def get_redis_connection():
    """Get Redis connection."""
    return redis.Redis(
        host=DatabaseConfig.REDIS_HOST,
        port=DatabaseConfig.REDIS_PORT,
        db=DatabaseConfig.REDIS_DB
    )


def get_postgres_connection(database=None):
    """Get PostgreSQL connection."""
    db = database or DatabaseConfig.PG_DATABASE
    return psycopg2.connect(
        host=DatabaseConfig.PG_HOST,
        port=DatabaseConfig.PG_PORT,
        database=db,
        user=DatabaseConfig.PG_USER,
        password=DatabaseConfig.PG_PASSWORD
    )


# Singleton instances for backward compatibility
r = get_redis_connection()


def connect_db(db_name):
    """Legacy function for backward compatibility."""
    return get_postgres_connection(db_name)
