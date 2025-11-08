import os, json, time, hashlib, datetime

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def _key_to_path(key):
    h = hashlib.sha256(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.json")

def _json_safe(obj):
    """Convert datetime and other non-serializable objects into strings."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)

def save(key, data, ttl=3600):
    path = _key_to_path(key)
    def make_serializable(o):
        if isinstance(o, dict):
            return {k: make_serializable(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [make_serializable(i) for i in o]
        else:
            return _json_safe(o)
    safe_data = make_serializable(data)
    payload = {"ts": time.time(), "ttl": ttl, "data": safe_data}
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)

def load(key):
    path = _key_to_path(key)
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            payload = json.load(f)
        if time.time() - payload.get("ts", 0) > payload.get("ttl", 0):
            os.remove(path)
            return None
        return payload.get("data")
    except Exception:
        return None
