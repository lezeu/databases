"""Redis connection module."""
from config import get_redis_connection

# Singleton instance for backward compatibility
r = get_redis_connection()

