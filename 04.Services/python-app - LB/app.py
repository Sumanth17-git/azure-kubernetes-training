from flask import Flask
import redis
import os

app = Flask(__name__)

# Read Redis host from environment variable
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = 6379

# Connect to Redis
r = redis.Redis(host=redis_host, port=redis_port)

@app.route("/")
def hello():
    try:
        count = r.incr("page_hits")
    except redis.exceptions.ConnectionError:
        return "⚠️ Could not connect to Redis", 500

    return f"👋 Hello! You've visited this page {count} times.\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
