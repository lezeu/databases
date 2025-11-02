from connection import r


def get_top_users(limit=10):
    """Get top N users from leaderboard"""
    # ZREVRANGE returns highest scores first
    top_users = r.zrevrange(
        "shopping:leaderboard", 0, limit - 1, withscores=True
    )  # type: ignore

    print(f"\n🏆 Top {limit} Shoppers:")
    print("-" * 50)
    for rank, (username, score) in enumerate(top_users, 1):  # type: ignore
        print(f"{rank}. {username:<20} ${score:,.2f}")

    return top_users


def get_user_rank(username):
    """Get a specific user's rank and score"""
    # ZREVRANK returns rank (0-indexed, highest first)
    rank = r.zrevrank("shopping:leaderboard", username)  # type: ignore
    score = r.zscore("shopping:leaderboard", username)  # type: ignore

    if rank is not None:
        print(f"\n📊 {username}'s Stats:")
        print(f"   Rank: #{rank + 1}")  # type: ignore
        print(f"   Total Spent: ${score:,.2f}")  # type: ignore
        return rank + 1, score  # type: ignore
    else:
        print(f"User {username} not found in leaderboard")
        return None, None


def get_users_in_range(min_score, max_score):
    """Get all users who spent between min and max"""
    users = r.zrangebyscore(
        "shopping:leaderboard", min_score, max_score, withscores=True
    )  # type: ignore

    print(
        f"\n💰 Users who spent between ${min_score:,.2f} and ${max_score:,.2f}:"
    )
    print("-" * 50)
    for username, score in users:  # type: ignore
        print(f"   {username:<20} ${score:,.2f}")

    return users


def get_leaderboard_size():
    """Get total number of users in leaderboard"""
    count = r.zcard("shopping:leaderboard")
    print(f"\n📈 Total users in leaderboard: {count}")
    return count
