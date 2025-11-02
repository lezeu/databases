"""
Basic Shopping Leaderboard using Redis Sorted Sets
This demonstrates the core leaderboard functionality
"""

import time
import matplotlib.pyplot as plt
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
        mapping={"total_spent": new_score, "last_updated": datetime.now().isoformat()},
    )
    print(f"✓ {username} made a purchase of ${amount}. New total: ${new_score:,.2f}")
    return new_score


# Example usage
if __name__ == "__main__":
    print("=" * 50)
    print("REDIS SHOPPING LEADERBOARD DEMO")
    print("=" * 50)

    # Performance tracking
    operation_times = {}

    # # Clear previous data (for demo purposes)
    # r.delete("shopping:leaderboard")
    #
    # # Add sample users
    # print("\n1. Adding users to leaderboard...")
    # start_time = time.time()
    # add_user_score(1, "Alice", 5000.00)
    # add_user_score(2, "Bob", 3500.50)
    # add_user_score(3, "Carol", 4200.75)
    # add_user_score(4, "David", 1800.00)
    # add_user_score(5, "Eve", 6500.25)
    # add_user_score(6, "Frank", 2900.00)
    # add_user_score(7, "Grace", 4800.50)
    # add_user_score(8, "Henry", 3200.00)
    # add_user_score(9, "Ivy", 5500.75)
    # add_user_score(10, "Jack", 2100.00)
    # operation_times["Add Users"] = time.time() - start_time

    # Get top users
    print("\n2. Getting top users...")
    start_time = time.time()
    get_top_users(5)
    operation_times["Get Top Users"] = time.time() - start_time

    # Get specific user's rank
    print("\n3. Checking Alice's rank...")
    start_time = time.time()
    get_user_rank("Alice")
    operation_times["Get User Rank"] = time.time() - start_time

    # Increment score (new purchase)
    print("\n4. Alice makes a new purchase...")
    start_time = time.time()
    increment_user_score("Alice", 1500.00)
    operation_times["Increment Score"] = time.time() - start_time

    # Check updated rank
    print("\n5. Checking Alice's updated rank...")
    start_time = time.time()
    get_user_rank("Alice")
    operation_times["Get Updated Rank"] = time.time() - start_time
    start_time = time.time()
    get_top_users(5)
    operation_times["Get Updated Top"] = time.time() - start_time

    # Delete a user
    print("\n6. Deleting user Alice...")
    start_time = time.time()
    delete_user("Alice")
    operation_times["Delete User"] = time.time() - start_time
    start_time = time.time()
    get_top_users(5)
    operation_times["Get Top After Delete"] = time.time() - start_time

    # Get users in spending range
    print("\n7. Finding users who spent $3000-$5000...")
    start_time = time.time()
    get_users_in_range(3000, 5000)
    operation_times["Get Users in Range"] = time.time() - start_time

    # Get leaderboard stats
    print("\n8. Leaderboard statistics...")
    start_time = time.time()
    get_leaderboard_size()
    operation_times["Get Leaderboard Size"] = time.time() - start_time

    # Performance plot
    print("\n9. Performance Results...")
    operations = list(operation_times.keys())
    times = [operation_times[op] * 1000 for op in operations]  # Convert to ms
    plt.figure(figsize=(10, 6))
    plt.bar(operations, times)
    plt.xlabel('Operations')
    plt.ylabel('Time (ms)')
    plt.title('Redis Operations Performance')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('performance_plot.png')
    plt.show()

    print("\n" + "=" * 50)
    print("Demo complete!")
    print("=" * 50)
