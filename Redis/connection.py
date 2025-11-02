import certifi
import os
import redis

HOST = 'LucianDB.redis.cache.windows.net'
PORT = 6380
PASSWORD = os.environ.get('REDIS_PASSWORD')

r = redis.StrictRedis(host=HOST, port=PORT, password=PASSWORD, ssl=True, ssl_ca_certs=certifi.where())
