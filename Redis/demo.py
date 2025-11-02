"""
Basic Shopping Leaderboard using Redis Sorted Sets
This demonstrates the core leaderboard functionality
"""

from datetime import datetime

from connection import r
from delete_member import delete_user
from insert_scores import add_user_score
from query_top import (
    get_leaderboard_size,
    get_top_users,
    get_user_rank,
    get_users_in_range,
)


def increment_user_score(username, amount):
    """Increment a user's score (when they make a new purchase)"""
    # ZINCRBY atomically increments the score
    new_score = r.zincrby("shopping:leaderboard", amount, username)
    # Update the hash with new total_spent and last_updated
    r.hset(
        f"user:{username}",
        mapping={
            "total_spent": new_score,
            "last_updated": datetime.now().isoformat()
        },
    )
    print(
        f"✓ {username} made a purchase of ${amount}. "
        f"New total: ${new_score:,.2f}"
    )
    return new_score


# Example usage
if __name__ == "__main__":
    print("=" * 50)
    print("REDIS SHOPPING LEADERBOARD DEMO")
    print("=" * 50)

    # Clear previous data (for demo purposes)
    r.delete("shopping:leaderboard")

    # Add sample users
    print("\n1. Adding users to leaderboard...")
    add_user_score(1, "Alice", 5000.00)
    add_user_score(2, "Bob", 3500.50)
    add_user_score(3, "Carol", 4200.75)
    add_user_score(4, "David", 1800.00)
    add_user_score(5, "Eve", 6500.25)
    add_user_score(6, "Frank", 2900.00)
    add_user_score(7, "Grace", 4800.50)
    add_user_score(8, "Henry", 3200.00)
    add_user_score(9, "Ivy", 5500.75)
    add_user_score(10, "Jack", 2100.00)

    # Get top users
    print("\n2. Getting top users...")
    get_top_users(5)

    # Get specific user's rank
    print("\n3. Checking Alice's rank...")
    get_user_rank("Alice")

    # Increment score (new purchase)
    print("\n4. Alice makes a new purchase...")
    increment_user_score("Alice", 1500.00)

    # Check updated rank
    print("\n5. Checking Alice's updated rank...")
    get_user_rank("Alice")
    get_top_users(5)

    # Delete a user
    print("\n5. Deleting user Alice...")
    delete_user("Alice")
    get_top_users(5)

    # Get users in spending range
    print("\n6. Finding users who spent $3000-$5000...")
    get_users_in_range(3000, 5000)

    # Get leaderboard stats
    print("\n7. Leaderboard statistics...")
    get_leaderboard_size()

    print("\n" + "=" * 50)
    print("Demo complete!")
    print("=" * 50)
