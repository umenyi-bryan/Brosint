"""
Simple filesystem cache: key -> JSON file with TTL (seconds).
Used to avoid repeated API calls during demos and development.
"""
import os, json, time, hashlib

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def _key_to_path(key):
    h = hashlib.sha256(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.json")

def save(key, data, ttl=3600):
    path = _key_to_path(key)
    payload = {"ts": time.time(), "ttl": ttl, "data": data}
    with open(path, "w") as f:
        json.dump(payload, f)

def load(key):
    path = _key_to_path(key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            payload = json.load(f)
        if time.time() - payload.get("ts",0) > payload.get("ttl",0):
            try: os.remove(path)
            except: pass
            return None
        return payload.get("data")
    except Exception:
        return None
