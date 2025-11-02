from connection import r


def delete_user(username):
    """Remove user from leaderboard"""
    result = r.zrem("shopping:leaderboard", username)
    if result:
        print(f"✓ Removed {username} from leaderboard")
    else:
        print(f"User {username} not found")
    return result
