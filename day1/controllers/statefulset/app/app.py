from flask import Flask, request
import redis
import os

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.StrictRedis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def home():
    count = r.incr('hits')
    return f"Welcome! This page has been visited {count} times."

@app.route('/set', methods=['POST'])
def set_key():
    key = request.args.get('key')
    value = request.args.get('value')
    r.set(key, value)
    return f"Key {key} set to {value}"

@app.route('/get')
def get_key():
    key = request.args.get('key')
    value = r.get(key)
    return f"Value for {key} is {value}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

