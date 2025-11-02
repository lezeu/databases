from connection import r

removed = r.zrem("leaderboard_shop", "User2") # Deleting one user

print(f"Removed {removed} member(s) from leaderboard_shop")
