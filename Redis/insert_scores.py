from connection import r

## Inserting sample data into a sorted set for a leaderboard
customers = { "User1": 120, "User2": 230, "User3": 180, "User4": 300 }

for name, score in customers.items():
    r.zadd("leaderboard_shop", {name: score})

print("Inserted scores into leaderboard_shop")
