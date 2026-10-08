import os
import socket
import redis
from flask import Flask

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

@app.route("/")
def home():
    versione = os.getenv("APP_VERSION", "1")
    try:
        visite = r.incr("visite")
    except redis.exceptions.ConnectionError:
        visite = "n/d (Redis non raggiungibile)"
    return f"Ciao! Versione {versione} - container: {socket.gethostname()} - visite: {visite}\n"

@app.route("/health")
def health():
    return "ok\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)