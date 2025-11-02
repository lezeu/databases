from connection import r
from datetime import datetime


def add_user_score(user_id, username, total_spent):
    """Add or update a user's score in the leaderboard"""
    # Store user details in a hash
    r.hset(f"user:{user_id}", mapping={
        "username": username,
        "total_spent": total_spent,
        "last_updated": datetime.now().isoformat()
    })

    # Add to sorted set (leaderboard)
    r.zadd("shopping:leaderboard", {username: total_spent})
    print(f"✓ Added {username} with score {total_spent}")
