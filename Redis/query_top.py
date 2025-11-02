from connection import r

## Retrieving top 3 customers from the leaderboard
top = r.zrevrange("leaderboard_shop", 0, 2, withscores=True)

print("TOP:")

for member, score in top:
    print(f"{member.decode()}: {int(score)} points")
